const { createApp, ref, computed, onMounted, nextTick } = Vue;

createApp({
  setup() {
    const skills = ref([]);
    const overview = ref({
      total_skills: 0,
      enabled_count: 0,
      disabled_count: 0,
      total_calls: 0,
      type_counts: {},
      top_skills: [],
      brain_sessions: 0
    });

    const selectedPlatform = ref('all'); // 'all' | 'antigravity' | 'claude' | 'codex'
    const searchQuery = ref('');
    const selectedType = ref('all');
    const selectedCategory = ref('all');
    const selectedStatus = ref('all');
    const sortBy = ref('created_at_desc'); // 默认按添加时间倒序
    const scanning = ref(false);
    const submitting = ref(false);

    const selectPlatform = (platform) => {
      selectedPlatform.value = platform;
      refreshIcons();
    };

    const detailSkill = ref(null);
    const docTab = ref('split'); // 默认且仅保留双语对照
    const translating = ref(false);
    const editingDoc = ref(null);
    const savingDoc = ref(false);

    // 双语对照同步滚动（默认开启，即时丝滑无死锁）
    const zhScrollRef = ref(null);
    const enScrollRef = ref(null);
    const syncScroll = ref(true); // 默认开启同步联动
    let syncSource = null;
    let syncTimer = null;

    const syncScrollBetween = (sourceEl, targetEl) => {
      if (!syncScroll.value || !sourceEl || !targetEl) return;
      const maxSrc = sourceEl.scrollHeight - sourceEl.clientHeight;
      const maxDst = targetEl.scrollHeight - targetEl.clientHeight;
      if (maxSrc > 0 && maxDst > 0) {
        const ratio = sourceEl.scrollTop / maxSrc;
        targetEl.scrollTop = ratio * maxDst;
      }
    };

    const onZhScroll = (e) => {
      if (!syncScroll.value) return;
      if (syncSource === 'en') return;
      syncSource = 'zh';
      clearTimeout(syncTimer);
      syncScrollBetween(zhScrollRef.value, enScrollRef.value);
      syncTimer = setTimeout(() => {
        syncSource = null;
      }, 60);
    };

    const onEnScroll = (e) => {
      if (!syncScroll.value) return;
      if (syncSource === 'zh') return;
      syncSource = 'en';
      clearTimeout(syncTimer);
      syncScrollBetween(enScrollRef.value, zhScrollRef.value);
      syncTimer = setTimeout(() => {
        syncSource = null;
      }, 60);
    };

    const showCreateModal = ref(false);
    const createMode = ref('form');
    const showTrashModal = ref(false);
    const trashItems = ref([]);
    const editingMeta = ref(null);

    const typeFilters = [
      { key: 'all', label: '全部' },
      { key: 'builtin', label: '内置 (Builtin)' },
      { key: 'global', label: '全局 (Global)' },
      { key: 'plugin', label: '插件 (Plugins)' },
      { key: 'workspace', label: '工作区 (Workspace)' },
    ];

    const newSkill = ref({
      name: '',
      description: '',
      chinese_summary: '',
      category: '代码开发',
      tags: [],
      content: '',
      target_type: 'global'
    });

    const gitForm = ref({
      repo_url: '',
      custom_name: ''
    });

    // 刷新 Lucide 图标
    const refreshIcons = () => {
      nextTick(() => {
        if (window.lucide) {
          window.lucide.createIcons();
        }
      });
    };

    // 格式化 Markdown
    const renderMarkdown = (text) => {
      if (!text) return '<p class="text-slate-500">（无正文内容）</p>';
      if (window.marked) {
        return window.marked.parse(text);
      }
      return text;
    };

    // 获取数据
    const loadOverview = async () => {
      try {
        const res = await fetch('/api/stats/overview');
        const json = await res.json();
        if (json.success) {
          overview.value = json.data;
        }
      } catch (e) {
        console.error('获取统计概览失败:', e);
      }
    };

    const loadSkills = async () => {
      try {
        const res = await fetch('/api/skills');
        const json = await res.json();
        if (json.success) {
          skills.value = json.data;
          refreshIcons();
        }
      } catch (e) {
        console.error('加载技能失败:', e);
      }
    };

    const loadTrash = async () => {
      try {
        const res = await fetch('/api/trash');
        const json = await res.json();
        if (json.success) {
          trashItems.value = json.data;
        }
      } catch (e) {
        console.error('加载回收站失败:', e);
      }
    };

    // 主动扫描刷新
    const triggerScan = async () => {
      scanning.value = true;
      try {
        const res = await fetch('/api/scan', { method: 'POST' });
        const json = await res.json();
        if (json.success) {
          skills.value = json.skills;
          await loadOverview();
          refreshIcons();
        }
      } catch (e) {
        alert('扫描失败: ' + e.message);
      } finally {
        scanning.value = false;
      }
    };

    // 启用/禁用切换
    const toggleSkill = async (skill) => {
      const orig = skill.is_enabled;
      skill.is_enabled = !orig; // 乐观UI更新
      try {
        const res = await fetch('/api/skills/toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skill_id: skill.id, enable: skill.is_enabled })
        });
        const json = await res.json();
        if (!json.success) {
          skill.is_enabled = orig;
          alert('操作失败: ' + (json.detail || json.message));
        } else {
          await loadOverview();
          refreshIcons();
        }
      } catch (e) {
        skill.is_enabled = orig;
        alert('请求异常: ' + e.message);
      }
    };

    // 删除至回收站
    const confirmDelete = async (skill) => {
      if (skill.type === 'builtin') {
        alert('系统内置核心技能受到保护，不可删除。如需停用请使用【禁用】开关！');
        return;
      }
      if (!confirm(`确定要将技能【${skill.name}】移入回收站吗？`)) {
        return;
      }
      try {
        const res = await fetch('/api/skills/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skill_id: skill.id })
        });
        const json = await res.json();
        if (json.success) {
          if (detailSkill.value && detailSkill.value.id === skill.id) {
            detailSkill.value = null;
          }
          await loadSkills();
          await loadOverview();
          await loadTrash();
        } else {
          alert('删除失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('删除异常: ' + e.message);
      }
    };

    // 回收站还原
    const restoreTrash = async (trashId) => {
      try {
        const res = await fetch('/api/trash/restore', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ trash_id: trashId })
        });
        const json = await res.json();
        if (json.success) {
          await loadTrash();
          await loadSkills();
          await loadOverview();
        } else {
          alert('还原失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('还原请求失败: ' + e.message);
      }
    };

    // 回收站彻底粉碎
    const purgeTrash = async (trashId) => {
      if (!confirm('彻底粉碎后将无法找回该技能文件，确认永久删除？')) return;
      try {
        const res = await fetch('/api/trash/purge', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ trash_id: trashId })
        });
        const json = await res.json();
        if (json.success) {
          await loadTrash();
        } else {
          alert('粉碎失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('请求失败: ' + e.message);
      }
    };

    // 打开详情
    const openDetail = (skill) => {
      detailSkill.value = skill;
      docTab.value = 'split';
      refreshIcons();

      // 重置左右双栏滚动位置至顶部
      nextTick(() => {
        if (zhScrollRef.value) zhScrollRef.value.scrollTop = 0;
        if (enScrollRef.value) enScrollRef.value.scrollTop = 0;
      });

      // 如果尚未翻译且存在英文正文，自动为用户开始预热翻译，提供无感极致体验
      if (!skill.chinese_body && skill.body) {
        translateCurrentSkill(false);
      }
    };

    // 翻译当前详情技能的 Markdown 正文
    const translateCurrentSkill = async (force = false) => {
      if (!detailSkill.value || translating.value) return;
      translating.value = true;
      try {
        const res = await fetch('/api/skills/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            skill_name: detailSkill.value.name,
            force: force
          })
        });
        const json = await res.json();
        if (json.success) {
          detailSkill.value.chinese_body = json.chinese_body;
          detailSkill.value.has_chinese_doc = true;
          // 同步到 skills 列表对应的对象
          const s = skills.value.find(item => item.name.toLowerCase() === detailSkill.value.name.toLowerCase());
          if (s) {
            s.chinese_body = json.chinese_body;
            s.has_chinese_doc = true;
          }
          refreshIcons();
        } else {
          alert('翻译失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('自动翻译请求异常: ' + e.message);
      } finally {
        translating.value = false;
        refreshIcons();
      }
    };

    // 打开编辑文档（tab 可选 'original' 英文原文 或 'zh' 中文译文）
    const openEditDoc = (skill, tab = 'original') => {
      editingDoc.value = {
        name: skill.name,
        tab: tab, // 'original' 或 'zh'
        originalContent: skill.body || '',
        zhContent: skill.chinese_body || '',
        skill: skill
      };
      refreshIcons();
    };

    // 保存编辑（支持保存英文原文写回本地物理文件，或保存中文对照译文）
    const saveDocContent = async () => {
      if (!editingDoc.value) return;
      savingDoc.value = true;
      const isOriginal = editingDoc.value.tab === 'original';
      const endpoint = isOriginal ? '/api/skills/save-original-doc' : '/api/skills/save-doc-translation';
      const content = isOriginal ? editingDoc.value.originalContent : editingDoc.value.zhContent;

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            skill_name: editingDoc.value.name,
            content: content,
            skill_id: detailSkill.value ? detailSkill.value.id : ''
          })
        });
        const json = await res.json();
        if (json.success) {
          const s = skills.value.find(item => item.name.toLowerCase() === editingDoc.value.name.toLowerCase());
          if (isOriginal) {
            const updatedBody = json.body || content;
            if (detailSkill.value && detailSkill.value.name.toLowerCase() === editingDoc.value.name.toLowerCase()) {
              detailSkill.value.body = updatedBody;
            }
            if (s) {
              s.body = updatedBody;
            }
            editingDoc.value = null;
            if (confirm('英文原文已成功写回本地 SKILL.md 物理文件！\n是否立即调用 Edge 端口重新生成最新中文对照？')) {
              translateCurrentSkill(true);
            }
          } else {
            if (detailSkill.value && detailSkill.value.name.toLowerCase() === editingDoc.value.name.toLowerCase()) {
              detailSkill.value.chinese_body = content;
              detailSkill.value.has_chinese_doc = true;
            }
            if (s) {
              s.chinese_body = content;
              s.has_chinese_doc = true;
            }
            editingDoc.value = null;
            alert('中文使用指南已成功保存！');
          }
        } else {
          alert('保存失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('保存异常: ' + e.message);
      } finally {
        savingDoc.value = false;
        refreshIcons();
      }
    };

    // 在系统资源管理器中打开并定位原始文件
    const openingFolder = ref(false);
    const openFolder = async (skillOrPath) => {
      const pathVal = typeof skillOrPath === 'object' ? (skillOrPath.path || '') : String(skillOrPath || '');
      const nameVal = typeof skillOrPath === 'object' ? (skillOrPath.name || '') : '';
      if (!pathVal && !nameVal) return;
      openingFolder.value = true;
      try {
        const res = await fetch('/api/skills/open-folder', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            path: pathVal,
            skill_name: nameVal
          })
        });
        const json = await res.json();
        if (!json.success) {
          alert('打开文件夹失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('打开文件夹请求异常: ' + e.message);
      } finally {
        setTimeout(() => {
          openingFolder.value = false;
        }, 1200);
      }
    };

    // 打开编辑元数据
    const openEditMeta = (skill) => {
      editingMeta.value = {
        name: skill.name,
        summary: skill.chinese_summary || '',
        category: skill.category || ''
      };
      refreshIcons();
    };

    // 保存元数据
    const saveMeta = async () => {
      if (!editingMeta.value) return;
      try {
        const res = await fetch('/api/skills/metadata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: editingMeta.value.name,
            summary: editingMeta.value.summary,
            category: editingMeta.value.category
          })
        });
        const json = await res.json();
        if (json.success) {
          // 同步前端数据
          const target = skills.value.find(s => s.name.toLowerCase() === editingMeta.value.name.toLowerCase());
          if (target) {
            target.chinese_summary = editingMeta.value.summary;
            target.category = editingMeta.value.category;
          }
          if (detailSkill.value && detailSkill.value.name.toLowerCase() === editingMeta.value.name.toLowerCase()) {
            detailSkill.value.chinese_summary = editingMeta.value.summary;
            detailSkill.value.category = editingMeta.value.category;
          }
          editingMeta.value = null;
        } else {
          alert('保存失败: ' + (json.detail || json.message));
        }
      } catch (e) {
        alert('保存异常: ' + e.message);
      }
    };

    // 打开新建模态框
    const openCreateModal = () => {
      newSkill.value = {
        name: '',
        description: '',
        chinese_summary: '',
        category: '代码开发',
        tags: [],
        content: '',
        target_type: 'global',
        platform: selectedPlatform.value !== 'all' ? selectedPlatform.value : 'antigravity'
      };
      gitForm.value = {
        repo_url: '',
        custom_name: '',
        platform: selectedPlatform.value !== 'all' ? selectedPlatform.value : 'antigravity'
      };
      showCreateModal.value = true;
      refreshIcons();
    };

    // 辅助解析 API 响应，防止返回 HTML/文本 500 导致 JSON 解析异常
    const parseApiResponse = async (res) => {
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch (err) {
        if (!res.ok) {
          throw new Error(`服务异常 (${res.status}): ${text.slice(0, 150)}`);
        }
        throw new Error(`数据格式异常: ${text.slice(0, 100)}`);
      }
    };

    // 提交创建或 Git 导入
    const submitCreate = async () => {
      submitting.value = true;
      try {
        if (createMode.value === 'form') {
          if (!newSkill.value.name) {
            alert('请输入技能标识名称 (Name)');
            return;
          }
          const res = await fetch('/api/skills/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newSkill.value)
          });
          const json = await parseApiResponse(res);
          if (json.success) {
            showCreateModal.value = false;
            await loadSkills();
            await loadOverview();
            alert(json.message || '技能创建成功！');
          } else {
            alert('创建失败: ' + (json.detail || json.message));
          }
        } else {
          if (!gitForm.value.repo_url) {
            alert('请输入 Git 仓库地址');
            return;
          }
          const res = await fetch('/api/skills/import-git', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(gitForm.value)
          });
          const json = await parseApiResponse(res);
          if (json.success) {
            showCreateModal.value = false;
            await loadSkills();
            await loadOverview();
            alert(json.message || 'Git 仓库导入技能成功！');
          } else {
            alert('导入失败: ' + (json.detail || json.message));
          }
        }
      } catch (e) {
        alert('操作异常: ' + e.message);
      } finally {
        submitting.value = false;
        refreshIcons();
      }
    };

    // 计算过滤与排序
    const filteredSkills = computed(() => {
      let list = [...skills.value];

      // 平台生态过滤
      if (selectedPlatform.value !== 'all') {
        list = list.filter(s => s.platform === selectedPlatform.value);
      }

      // 搜索过滤
      if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase().trim();
        list = list.filter(s => 
          s.name.toLowerCase().includes(q) ||
          (s.chinese_summary && s.chinese_summary.toLowerCase().includes(q)) ||
          (s.description && s.description.toLowerCase().includes(q)) ||
          (s.tags && s.tags.some(t => t.toLowerCase().includes(q))) ||
          (s.category && s.category.toLowerCase().includes(q))
        );
      }

      // 类型过滤
      if (selectedType.value !== 'all') {
        list = list.filter(s => s.type === selectedType.value);
      }

      // 中文领域分类过滤
      if (selectedCategory.value !== 'all') {
        list = list.filter(s => s.category === selectedCategory.value);
      }

      // 状态过滤
      if (selectedStatus.value === 'enabled') {
        list = list.filter(s => s.is_enabled);
      } else if (selectedStatus.value === 'disabled') {
        list = list.filter(s => !s.is_enabled);
      }

      // 排序
      if (sortBy.value === 'created_at_desc') {
        list.sort((a, b) => (b.created_timestamp || 0) - (a.created_timestamp || 0));
      } else if (sortBy.value === 'created_at_asc') {
        list.sort((a, b) => (a.created_timestamp || 0) - (b.created_timestamp || 0));
      } else if (sortBy.value === 'call_count_desc') {
        list.sort((a, b) => b.call_count - a.call_count);
      } else if (sortBy.value === 'name_asc') {
        list.sort((a, b) => a.name.localeCompare(b.name));
      } else if (sortBy.value === 'name_desc') {
        list.sort((a, b) => b.name.localeCompare(a.name));
      } else if (sortBy.value === 'status') {
        list.sort((a, b) => (b.is_enabled ? 1 : 0) - (a.is_enabled ? 1 : 0));
      }

      return list;
    });

    // 平台统计
    const platformCounts = computed(() => {
      const counts = { all: skills.value.length, antigravity: 0, claude: 0, codex: 0 };
      skills.value.forEach(s => {
        const p = s.platform || 'antigravity';
        if (counts[p] !== undefined) counts[p]++;
      });
      return counts;
    });

    // 动态概览统计卡片数据 (随选中的平台自适应联动)
    const activeOverview = computed(() => {
      const currentList = selectedPlatform.value === 'all' 
        ? skills.value 
        : skills.value.filter(s => s.platform === selectedPlatform.value);
      
      const total = currentList.length;
      const enabled = currentList.filter(s => s.is_enabled).length;
      const disabled = total - enabled;
      const translated = currentList.filter(s => s.has_chinese_doc).length;

      const typeCounts = {};
      currentList.forEach(s => {
        typeCounts[s.type] = (typeCounts[s.type] || 0) + 1;
      });

      return {
        total_skills: total,
        enabled_count: enabled,
        disabled_count: disabled,
        translated_count: translated,
        type_counts: typeCounts,
        total_calls: currentList.reduce((acc, s) => acc + (s.call_count || 0), 0)
      };
    });

    const availableCategories = computed(() => {
      const set = new Set();
      skills.value.forEach(s => {
        if (s.category) set.add(s.category);
      });
      return Array.from(set).sort();
    });

    const trashCount = computed(() => trashItems.value.length);
    const topSkillName = computed(() => {
      if (overview.value.top_skills && overview.value.top_skills.length > 0) {
        return overview.value.top_skills[0].name;
      }
      return '暂无';
    });

    const getPlatformBadgeClass = (platform) => {
      switch(platform) {
        case 'antigravity': return 'bg-emerald-50 text-emerald-700 border-emerald-200/80';
        case 'claude': return 'bg-amber-50 text-amber-700 border-amber-200/80';
        case 'codex': return 'bg-indigo-50 text-indigo-700 border-indigo-200/80';
        default: return 'bg-slate-100 text-slate-700 border-slate-200';
      }
    };

    const getPlatformLabel = (platform) => {
      switch(platform) {
        case 'antigravity': return 'Antigravity';
        case 'claude': return 'Claude Code';
        case 'codex': return 'Codex';
        default: return 'Antigravity';
      }
    };

    const getTypeBadgeClass = (type) => {
      switch(type) {
        case 'builtin': return 'bg-sky-50 text-sky-700 border-sky-200/80';
        case 'global': return 'bg-emerald-50 text-emerald-700 border-emerald-200/80';
        case 'plugin': return 'bg-purple-50 text-purple-700 border-purple-200/80';
        case 'workspace': return 'bg-amber-50 text-amber-700 border-amber-200/80';
        case 'vendor': return 'bg-indigo-50 text-indigo-700 border-indigo-200/80';
        default: return 'bg-slate-100 text-slate-600 border-slate-200/80';
      }
    };

    const getTypeLabel = (type, pluginName) => {
      switch(type) {
        case 'builtin': return '系统内置';
        case 'global': return '全局技能';
        case 'plugin': return pluginName ? `插件: ${pluginName}` : '插件扩展';
        case 'workspace': return '当前工作区';
        case 'vendor': return '厂商预置';
        default: return type;
      }
    };

    onMounted(async () => {
      await loadSkills();
      await loadOverview();
      await loadTrash();
      refreshIcons();
    });

    const exitApp = async () => {
      if (!confirm('确定要退出 AI Coding 技能管理器后台服务吗？退出后可随时通过快捷方式再次打开。')) {
        return;
      }
      try {
        await fetch(`${API_BASE}/app/exit`, { method: 'POST' });
      } catch (e) {
        // 服务立即退出可能导致 fetch 提前中断，属于正常现象
      }
      document.body.innerHTML = `
        <div style="height:100vh;display:flex;align-items:center;justify-content:center;font-family:system-ui,-apple-system,sans-serif;background:#f8fafc;color:#64748b;text-align:center;padding:24px;">
          <div style="background:white;padding:32px;border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,0.06);border:1px solid #e2e8f0;max-width:400px;">
            <div style="width:48px;height:48px;background:#f1f5f9;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 16px auto;font-size:24px;">👋</div>
            <h2 style="font-size:18px;font-weight:700;color:#0f172a;margin-bottom:8px;">服务已安全退出</h2>
            <p style="font-size:13px;line-height:1.6;color:#64748b;margin:0;">您可以安全关闭此浏览器标签页。<br>如需再次使用，双击桌面快捷方式即可秒级唤醒。</p>
          </div>
        </div>
      `;
    };

    return {
      exitApp,
      selectedPlatform,
      selectPlatform,
      platformCounts,
      activeOverview,
      getPlatformBadgeClass,
      getPlatformLabel,
      skills,
      overview,
      searchQuery,
      selectedType,
      selectedCategory,
      availableCategories,
      selectedStatus,
      sortBy,
      scanning,
      submitting,
      detailSkill,
      docTab,
      translating,
      editingDoc,
      savingDoc,
      zhScrollRef,
      enScrollRef,
      syncScroll,
      onZhScroll,
      onEnScroll,
      translateCurrentSkill,
      openEditDoc,
      saveDocContent,
      saveDocTranslation: saveDocContent,
      showCreateModal,
      createMode,
      showTrashModal,
      trashItems,
      trashCount,
      editingMeta,
      typeFilters,
      newSkill,
      gitForm,
      filteredSkills,
      topSkillName,
      refreshIcons,
      renderMarkdown,
      triggerScan,
      toggleSkill,
      confirmDelete,
      restoreTrash,
      purgeTrash,
      openDetail,
      openEditMeta,
      saveMeta,
      openCreateModal,
      submitCreate,
      openFolder,
      openingFolder,
      getTypeBadgeClass,
      getTypeLabel
    };
  }
}).mount('#app');
