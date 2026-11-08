/**
 * RCMB MOB AI - Frontend Application Controller (V3 - Clean UI, Fixed Chatbot & Role Hubs)
 * Regional College of Management Bangalore
 * Exclusively MBA & PGDM Programs
 */

document.addEventListener("DOMContentLoaded", () => {
  // App State
  let currentUser = null;
  let activeTimetableDay = "Monday";
  let activeTimetableProgram = "PGDM";

  // Elements
  const landingView = document.getElementById("landing-view");
  const portalView = document.getElementById("portal-view");
  const authModal = document.getElementById("auth-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const authTabLogin = document.getElementById("auth-tab-login");
  const authTabRegister = document.getElementById("auth-tab-register");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const toastEl = document.getElementById("toast-notification");

  // Portal Elements
  const portalUserInitials = document.getElementById("portal-user-initials");
  const portalUserName = document.getElementById("portal-user-name");
  const portalUserProgram = document.getElementById("portal-user-program");
  const navUserBadge = document.getElementById("nav-user-badge");
  const navAuthBtns = document.getElementById("nav-auth-btns");
  const navUserMenu = document.getElementById("nav-user-menu");

  // 3-Dot Menu Elements
  const threeDotsBtn = document.getElementById("three-dots-toggle-btn");
  const threeDotsMenu = document.getElementById("three-dots-dropdown-menu");

  // Chat Elements
  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const chatSendBtn = document.getElementById("chat-send-btn");

  // Initialize
  checkAuth();
  setupEventListeners();
  initTimetableDay();

  // ----------------- Authentication Logic -----------------

  async function checkAuth() {
    try {
      const res = await fetch("/api/auth/me");
      const data = await res.json();
      if (data.authenticated && data.user) {
        setUser(data.user);
      } else {
        const stored = localStorage.getItem("rcmb_user");
        if (stored) {
          try {
            setUser(JSON.parse(stored));
          } catch (e) {
            clearUser();
          }
        } else {
          clearUser();
        }
      }
    } catch (err) {
      const stored = localStorage.getItem("rcmb_user");
      if (stored) setUser(JSON.parse(stored));
    }
  }

  function setUser(user) {
    currentUser = user;
    localStorage.setItem("rcmb_user", JSON.stringify(user));
    activeTimetableProgram = user.program || "PGDM";

    landingView.style.display = "none";
    portalView.style.display = "block";

    portalUserInitials.textContent = user.avatar_initials || "ST";
    portalUserName.textContent = user.full_name;
    portalUserProgram.textContent = `${user.program} • ${user.section || 'Sec A'}`;

    navAuthBtns.style.display = "none";
    navUserMenu.style.display = "flex";
    navUserBadge.textContent = `${user.full_name.split(' ')[0]} (${user.role.toUpperCase()})`;

    // Configure Role-Specific Dashboards
    configureRoleDashboard(user);

    // Default to Chatbot View
    switchPortalView("chatbot-view");

    // Load data
    loadTimetable(activeTimetableProgram, activeTimetableDay);
    loadAttendance();
    loadAssignments();
    loadNotifications();

    document.getElementById("profile-name-input").value = user.full_name;
    document.getElementById("profile-mobile-input").value = user.mobile;
    document.getElementById("profile-email-input").value = user.email;
    document.getElementById("profile-program-input").value = user.program;
  }

  function clearUser() {
    currentUser = null;
    localStorage.removeItem("rcmb_user");
    landingView.style.display = "block";
    portalView.style.display = "none";
    navAuthBtns.style.display = "flex";
    navUserMenu.style.display = "none";
  }

  // Distinct Dashboard Hubs for Faculty and CEO
  function configureRoleDashboard(user) {
    const facultyHub = document.getElementById("faculty-dashboard-hub");
    const ceoHub = document.getElementById("ceo-dashboard-hub");
    const facultyCourse = document.getElementById("faculty-course-name");

    facultyHub.style.display = "none";
    ceoHub.style.display = "none";

    if (user.role === "faculty") {
      facultyHub.style.display = "block";
      if (user.email.includes("ashim")) {
        if (facultyCourse) facultyCourse.textContent = "AI & Its Applications";
      } else {
        if (facultyCourse) facultyCourse.textContent = "Communication Skills & OB";
      }
    } else if (user.role === "ceo") {
      ceoHub.style.display = "block";
    }
  }

  function showToast(message, type = "success") {
    toastEl.textContent = message;
    toastEl.className = `toast-msg ${type}`;
    toastEl.style.display = "block";
    setTimeout(() => {
      toastEl.style.display = "none";
    }, 4000);
  }

  function openAuthModal(mode = "login", defaultEmail = "") {
    authModal.classList.add("active");
    if (defaultEmail) {
      document.getElementById("login-email").value = defaultEmail;
    }
    if (mode === "login") {
      authTabLogin.classList.add("active");
      authTabRegister.classList.remove("active");
      loginForm.style.display = "block";
      registerForm.style.display = "none";
    } else {
      authTabRegister.classList.add("active");
      authTabLogin.classList.remove("active");
      registerForm.style.display = "block";
      loginForm.style.display = "none";
    }
  }

  function closeAuthModal() {
    authModal.classList.remove("active");
  }

  // ----------------- Event Listeners -----------------
  function setupEventListeners() {
    document.querySelectorAll(".btn-open-login").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        openAuthModal("login");
      });
    });

    document.querySelectorAll(".btn-open-register").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        openAuthModal("register");
      });
    });

    // Clean Landing Page Role Card Clicks (Student, Faculty, CEO)
    document.querySelectorAll(".btn-open-role-login").forEach(card => {
      card.addEventListener("click", (e) => {
        e.preventDefault();
        const role = card.getAttribute("data-role");
        if (currentUser) {
          showToast(`Active Session: ${currentUser.full_name} (${currentUser.role})`);
          landingView.style.display = "none";
          portalView.style.display = "block";
        } else {
          let emailHint = "satish@rcmb.edu.in";
          if (role === "faculty") emailHint = "tapas.panda@rcmb.edu.in";
          if (role === "ceo") emailHint = "jay.mandal@rcmb.edu.in";
          openAuthModal("login", emailHint);
        }
      });
    });

    // Top Header Instant Demo Buttons
    document.querySelectorAll(".btn-instant-demo").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const email = btn.getAttribute("data-email");
        const pw = btn.getAttribute("data-pw");
        handleLoginSubmit(email, pw);
      });
    });

    // 3-Dot Menu Toggle
    if (threeDotsBtn && threeDotsMenu) {
      threeDotsBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        threeDotsMenu.classList.toggle("active");
      });

      document.addEventListener("click", (e) => {
        if (!threeDotsMenu.contains(e.target) && e.target !== threeDotsBtn) {
          threeDotsMenu.classList.remove("active");
        }
      });
    }

    // View Switching (from 3-dot dropdown or quick pills)
    document.querySelectorAll("[data-view]").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const viewId = btn.getAttribute("data-view");
        if (viewId) {
          switchPortalView(viewId);
          if (threeDotsMenu) threeDotsMenu.classList.remove("active");
        }
      });
    });

    modalCloseBtn.addEventListener("click", closeAuthModal);
    authModal.addEventListener("click", (e) => {
      if (e.target === authModal) closeAuthModal();
    });

    authTabLogin.addEventListener("click", () => openAuthModal("login"));
    authTabRegister.addEventListener("click", () => openAuthModal("register"));

    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value.trim();
      const password = document.getElementById("login-password").value;
      handleLoginSubmit(email, password);
    });

    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fullName = document.getElementById("reg-name").value.trim();
      const email = document.getElementById("reg-email").value.trim();
      const mobile = document.getElementById("reg-mobile").value.trim();
      const program = document.getElementById("reg-program").value;
      const section = document.getElementById("reg-section").value;
      const password = document.getElementById("reg-password").value;
      const confirmPassword = document.getElementById("reg-confirm-password").value;

      if (password !== confirmPassword) {
        showToast("Passwords do not match. Please re-enter.", "error");
        return;
      }

      try {
        const res = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: fullName,
            email: email,
            mobile: mobile,
            program: program,
            section: section,
            password: password
          })
        });
        const data = await res.json();
        if (data.success) {
          showToast(data.message, "success");
          closeAuthModal();
          setUser(data.user);
        } else {
          showToast(data.error || "Failed to create account", "error");
        }
      } catch (err) {
        showToast("Network error. Please try again.", "error");
      }
    });

    document.querySelectorAll(".btn-logout").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        e.preventDefault();
        try {
          await fetch("/api/auth/logout", { method: "POST" });
        } catch (e) {}
        clearUser();
        showToast("Signed out successfully.");
      });
    });

    document.querySelectorAll(".brand-wrapper").forEach(brand => {
      brand.addEventListener("click", () => {
        if (currentUser) {
          switchPortalView("chatbot-view");
        } else {
          landingView.style.display = "block";
          portalView.style.display = "none";
        }
      });
    });

    chatSendBtn.addEventListener("click", sendChatMessage);
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendChatMessage();
    });

    document.querySelectorAll(".query-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        const queryText = chip.getAttribute("data-query");
        if (queryText) {
          chatInput.value = queryText;
          sendChatMessage();
        }
      });
    });

    document.querySelectorAll(".day-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".day-tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeTimetableDay = btn.getAttribute("data-day");
        loadTimetable(activeTimetableProgram, activeTimetableDay);
      });
    });

    document.querySelectorAll(".program-pill-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".program-pill-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeTimetableProgram = btn.getAttribute("data-program");
        loadTimetable(activeTimetableProgram, activeTimetableDay);
      });
    });

    const datePicker = document.getElementById("timetable-date-picker");
    if (datePicker) {
      datePicker.addEventListener("change", (e) => {
        const dateVal = e.target.value;
        if (dateVal) {
          const d = new Date(dateVal);
          const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
          const selectedDay = days[d.getDay()];
          activeTimetableDay = selectedDay === "Sunday" ? "Monday" : selectedDay;
          
          document.querySelectorAll(".day-tab-btn").forEach(b => {
            if (b.getAttribute("data-day") === activeTimetableDay) {
              b.classList.add("active");
            } else {
              b.classList.remove("active");
            }
          });
          loadTimetable(activeTimetableProgram, activeTimetableDay);
          showToast(`Showing schedule for ${selectedDay} (${dateVal})`);
        }
      });
    }

    const profileForm = document.getElementById("profile-form");
    if (profileForm) {
      profileForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const full_name = document.getElementById("profile-name-input").value.trim();
        const mobile = document.getElementById("profile-mobile-input").value.trim();
        const password = document.getElementById("profile-pw-input").value;

        try {
          const res = await fetch("/api/auth/update_profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, mobile, password })
          });
          const data = await res.json();
          if (data.success) {
            setUser(data.user);
            showToast("Profile details updated successfully!", "success");
          } else {
            showToast(data.error || "Update failed", "error");
          }
        } catch (err) {
          showToast("Network error while updating profile", "error");
        }
      });
    }
  }

  async function handleLoginSubmit(email, password) {
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, "success");
        closeAuthModal();
        setUser(data.user);
      } else {
        showToast(data.error || "Invalid credentials", "error");
      }
    } catch (err) {
      showToast("Unable to reach authentication server.", "error");
    }
  }

  // Switch Portal View Cleanly
  function switchPortalView(viewKey) {
    const viewMap = {
      "chatbot-view": "view-chatbot",
      "timetable-view": "view-timetable",
      "attendance-view": "view-attendance",
      "assignments-view": "view-assignments",
      "notifications-view": "view-notifications",
      "gallery-view": "view-gallery",
      "profile-view": "view-profile"
    };

    const targetId = viewMap[viewKey] || "view-chatbot";

    // Hide all portal views
    document.querySelectorAll(".portal-module-view").forEach(v => {
      v.style.display = "none";
    });

    // Show target view
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      targetEl.style.display = "block";
    }

    // Update quick tab pills in top bar
    document.querySelectorAll(".portal-tab-pill").forEach(p => {
      if (p.getAttribute("data-view") === viewKey) {
        p.classList.add("active");
      } else {
        p.classList.remove("active");
      }
    });
  }

  function initTimetableDay() {
    const today = new Date();
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const currentDay = days[today.getDay()];
    activeTimetableDay = currentDay === "Sunday" ? "Monday" : currentDay;
    
    document.querySelectorAll(".day-tab-btn").forEach(btn => {
      if (btn.getAttribute("data-day") === activeTimetableDay) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }

  // ----------------- Chatbot Execution with 1.6s Thinking Effect -----------------
  async function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage(text, "user");
    chatInput.value = "";

    const thinkingId = appendThinkingIndicator();
    const startTime = Date.now();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          email: currentUser ? currentUser.email : "satish@rcmb.edu.in",
          program: currentUser ? currentUser.program : "PGDM"
        })
      });
      const data = await res.json();

      const elapsed = Date.now() - startTime;
      const remainingDelay = Math.max(0, 1600 - elapsed);

      setTimeout(() => {
        removeElement(thinkingId);
        if (data.success) {
          appendBotResponse(data);
        } else {
          appendMessage(data.answer || "I encountered an error. Please ask again.", "bot");
        }
      }, remainingDelay);

    } catch (err) {
      setTimeout(() => {
        removeElement(thinkingId);
        appendMessage("Network connection interrupted. Please try asking again.", "bot");
      }, 1000);
    }
  }

  function appendMessage(text, sender = "bot") {
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${sender}`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = formatMarkdown(text);

    const time = document.createElement("div");
    time.className = "message-time";
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    bubble.appendChild(content);
    bubble.appendChild(time);
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendThinkingIndicator() {
    const id = "thinking-" + Date.now();
    const bubble = document.createElement("div");
    bubble.id = id;
    bubble.className = "bot-thinking-bubble";
    bubble.innerHTML = `
      <i class="fa-solid fa-brain thinking-icon"></i>
      <div class="thinking-text-wrap">
        <span class="thinking-title">RCMB MOB AI is thinking...</span>
        <span class="thinking-dots-anim">
          <span>Synthesizing official timetable</span>
          <span class="dot-bounce"></span>
          <span class="dot-bounce"></span>
          <span class="dot-bounce"></span>
        </span>
      </div>
    `;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
  }

  function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function appendBotResponse(data) {
    const bubble = document.createElement("div");
    bubble.className = "message-bubble bot";

    const content = document.createElement("div");
    content.className = "message-content";

    let html = formatMarkdown(data.answer);

    if (data.schedule && data.schedule.length > 0) {
      html += `<div class="chat-timetable-card-list">`;
      data.schedule.forEach(item => {
        const isBreak = item.is_break === 1;
        html += `
          <div class="chat-timetable-slot-card" style="${isBreak ? 'border-left-color: #C8963E; background: #FFFBF2;' : ''}">
            <div class="slot-header">
              <span class="slot-time-badge"><i class="fa-regular fa-clock"></i> ${item.slot_code ? item.slot_code + ' • ' : ''}${item.time_slot}</span>
              <span class="slot-room-badge"><i class="fa-solid fa-location-dot"></i> ${item.room}</span>
            </div>
            <div class="slot-subject-title">${item.subject}</div>
            ${item.faculty ? `<div class="slot-faculty-row"><i class="fa-solid fa-chalkboard-user"></i> <strong>Faculty:</strong> ${item.faculty}</div>` : ''}
          </div>
        `;
      });
      html += `</div>`;
    }

    content.innerHTML = html;

    const time = document.createElement("div");
    time.className = "message-time";
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    bubble.appendChild(content);
    bubble.appendChild(time);
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function formatMarkdown(text) {
    if (!text) return "";
    let str = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    str = str.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    str = str.replace(/\*(.*?)\*/g, "<em>$1</em>");
    str = str.replace(/^• (.*$)/gim, "<li style='margin-left: 1.2rem;'>$1</li>");
    str = str.replace(/^> (.*$)/gim, "<blockquote style='border-left: 3px solid #8B1D24; padding-left: 0.8rem; margin: 0.5rem 0; color: #57534E; font-style: italic;'>$1</blockquote>");
    str = str.replace(/\n\n/g, "<br><br>");
    str = str.replace(/\n/g, "<br>");
    return str;
  }

  // ----------------- Timetable Explorer Loader -----------------
  async function loadTimetable(program, day) {
    const container = document.getElementById("timetable-grid-cards");
    if (!container) return;

    container.innerHTML = `<div style="text-align: center; padding: 2rem; color: #78716C;"><i class="fa-solid fa-spinner fa-spin"></i> Loading ${program} ${day} Schedule...</div>`;

    try {
      const res = await fetch(`/api/timetable?program=${program}&day=${day}`);
      const data = await res.json();
      
      if (!data.schedule || data.schedule.length === 0) {
        container.innerHTML = `
          <div style="background: #FFFFFF; border: 1px solid #E7E0D8; border-radius: 16px; padding: 2.5rem; text-align: center;">
            <i class="fa-solid fa-calendar-xmark" style="font-size: 2.5rem; color: #8B1D24; margin-bottom: 0.75rem;"></i>
            <h4 style="font-weight: 800; font-size: 1.15rem; color: #1F2937;">No Classes Scheduled</h4>
            <p style="color: #78716C; margin-top: 0.25rem;">Sunday is the weekly campus off. Library is open from 10:00 AM to 5:00 PM.</p>
          </div>
        `;
        return;
      }

      let html = "";
      data.schedule.forEach(item => {
        const isBreak = item.is_break === 1;
        html += `
          <div class="schedule-card-full ${isBreak ? 'break-slot' : ''}">
            <div class="schedule-time-col">
              <span class="schedule-period-tag">${item.slot_code}</span>
              <span class="schedule-time-text">${item.time_slot}</span>
            </div>
            <div class="schedule-info-col">
              <h3>${item.subject}</h3>
              <p><i class="fa-solid ${isBreak ? 'fa-mug-hot' : 'fa-chalkboard-user'}" style="color: ${isBreak ? '#C8963E' : '#8B1D24'};"></i> <strong>${item.faculty}</strong></p>
            </div>
            <div class="schedule-room-col">
              <span class="schedule-room-badge"><i class="fa-solid fa-location-dot" style="color: #8B1D24;"></i> ${item.room}</span>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div style="color: #EF4444; padding: 1.5rem;">Failed to load timetable schedule.</div>`;
    }
  }

  // ----------------- Attendance Loader (CLEAN UI - ZERO OVERLAP) -----------------
  async function loadAttendance() {
    const listEl = document.getElementById("attendance-subject-list");
    const overallEl = document.getElementById("attendance-overall-pct");
    const totalEl = document.getElementById("attendance-total-classes");
    const attendedEl = document.getElementById("attendance-attended-classes");
    if (!listEl) return;

    try {
      const email = currentUser ? currentUser.email : "satish@rcmb.edu.in";
      const res = await fetch(`/api/attendance?email=${encodeURIComponent(email)}`);
      const data = await res.json();

      overallEl.textContent = `${data.overall_percentage}%`;
      totalEl.textContent = `${data.total_classes}`;
      attendedEl.textContent = `${data.attended_classes}`;

      let html = "";
      data.records.forEach(r => {
        const isEligible = r.percentage >= 75;
        const color = isEligible ? "#059669" : "#DC2626";
        html += `
          <div class="subject-row-clean">
            <div class="sub-left-col">
              <div class="sub-title-clean">${r.subject}</div>
              <div class="sub-ratio-clean">Conducted: <strong>${r.total_classes}</strong> sessions • Attended: <strong>${r.attended_classes}</strong> sessions</div>
              <div class="sub-progress-track">
                <div class="sub-progress-fill" style="width: ${r.percentage}%; background: ${color};"></div>
              </div>
            </div>
            <div class="sub-right-col">
              <div class="sub-pct-badge" style="color: ${color};">${r.percentage}%</div>
              <div style="font-size: 0.72rem; font-weight: 700; color: ${color}; margin-top: 0.15rem;">
                ${isEligible ? 'Eligible' : 'Shortage'}
              </div>
            </div>
          </div>
        `;
      });
      listEl.innerHTML = html;
    } catch (err) {
      listEl.innerHTML = `<div style="color: #EF4444;">Could not load attendance details.</div>`;
    }
  }

  // ----------------- Assignments Loader -----------------
  async function loadAssignments() {
    const container = document.getElementById("assignments-list-container");
    if (!container) return;

    try {
      const prog = currentUser ? currentUser.program : "PGDM";
      const res = await fetch(`/api/assignments?program=${prog}`);
      const data = await res.json();

      let html = "";
      data.assignments.forEach(a => {
        const isSubmitted = a.status === "Submitted";
        html += `
          <div style="background: #FFFFFF; border: 1px solid #E7E0D8; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 0.85rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <span style="background: rgba(139, 29, 36, 0.08); color: #8B1D24; padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">${a.subject}</span>
              <h4 style="font-weight: 800; font-size: 1.05rem; color: #1F2937; margin-top: 0.4rem;">${a.title}</h4>
              <p style="font-size: 0.82rem; color: #78716C; margin-top: 0.2rem;">Evaluator: <strong>${a.faculty}</strong> • Deadline: <strong style="color: #1F2937;">${a.due_date}</strong></p>
            </div>
            <div>
              <span style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.85rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; background: ${isSubmitted ? '#D1FAE5' : '#FEF3C7'}; color: ${isSubmitted ? '#065F46' : '#92400E'};">
                <i class="fa-solid ${isSubmitted ? 'fa-circle-check' : 'fa-clock'}"></i> ${a.status}
              </span>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div style="color: #EF4444;">Could not load assignments.</div>`;
    }
  }

  // ----------------- Notifications Loader -----------------
  async function loadNotifications() {
    const container = document.getElementById("notifications-list-container");
    if (!container) return;

    try {
      const res = await fetch("/api/notifications");
      const data = await res.json();

      let html = "";
      data.notifications.forEach(n => {
        html += `
          <div style="background: #FFFFFF; border: 1px solid #E7E0D8; border-radius: 14px; padding: 1.3rem 1.6rem; margin-bottom: 0.85rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
              <span style="background: #F4EFEB; border: 1px solid #E7E0D8; padding: 0.2rem 0.65rem; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; color: #8B1D24;">${n.category}</span>
              <span style="font-size: 0.75rem; color: #78716C;"><i class="fa-regular fa-clock"></i> ${n.date}</span>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 800; color: #1F2937;">${n.title}</h4>
            <p style="font-size: 0.88rem; color: #57534E; margin-top: 0.35rem; line-height: 1.5;">${n.content}</p>
          </div>
        `;
      });
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div style="color: #EF4444;">Could not load announcements.</div>`;
    }
  }

  // ----------------- PWA Service Worker Registration -----------------
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/sw.js')
        .then(reg => console.log('RCMB PWA Service Worker active:', reg.scope))
        .catch(err => console.log('Service Worker registration note:', err));
    });
  }

  let deferredPrompt;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    const installBtn = document.getElementById('pwa-install-app-btn');
    if (installBtn) {
      installBtn.style.display = 'inline-flex';
      installBtn.addEventListener('click', () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            showToast('Installing RCMB mob AI App...');
          }
          deferredPrompt = null;
        });
      });
    }
  });
});
