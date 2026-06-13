let currentRole = null;
let currentStep = 1;

const farmerPerks = [
  'Complete your farm profile to attract investors',
  'Set up your first crop listing',
  'Join the AgroVest farmer community',
  'Access free agri-business training resources'
];
const investorPerks = [
  'Browse active farm investment opportunities',
  'Set up your wallet and funding preferences',
  'Enable harvest & payout notifications',
  'View your portfolio dashboard'
];

function selectRole(role) {
  currentRole = role;
  document.getElementById('card-farmer').classList.remove('selected');
  document.getElementById('card-investor').classList.remove('selected');
  document.getElementById('card-' + role).classList.add('selected');

  const btn = document.getElementById('btn-step1');
  btn.disabled = false;
  if (role === 'investor') {
    btn.classList.add('inv');
  } else {
    btn.classList.remove('inv');
  }
}

function goStep(n) {
  document.getElementById('step-' + currentStep).classList.remove('active');
  currentStep = n;
  document.getElementById('step-' + n).classList.add('active');
  updateProgress(n);
  updateStepDots(n);

  if (n === 2) {
    if (currentRole === 'investor') {
      document.getElementById('farmer-fields').style.display  = 'none';
      document.getElementById('investor-fields').style.display = 'block';
      document.getElementById('step2-heading').innerHTML = 'Investor<br><em>details.</em>';
      document.getElementById('step2-sub').textContent   = 'Tell us about yourself so we can tailor your investment experience.';
      document.getElementById('btn-step2').classList.add('inv');
    } else {
      document.getElementById('farmer-fields').style.display  = 'block';
      document.getElementById('investor-fields').style.display = 'none';
      document.getElementById('step2-heading').innerHTML = 'Farmer<br><em>details.</em>';
      document.getElementById('step2-sub').textContent   = 'Tell us about your farm so we can build your profile.';
      document.getElementById('btn-step2').classList.remove('inv');
    }
  }

  if (n === 3 && currentRole === 'investor') {
    document.getElementById('btn-step3').classList.add('inv');
  }

  if (n === 4) {
    const perks = currentRole === 'farmer' ? farmerPerks : investorPerks;
    const el = document.getElementById('success-perks');
    el.innerHTML = perks.map(p => `
      <div class="success-perk">
        <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
          <polyline points="2 7 5.5 10.5 12 3.5"/>
        </svg>
        ${p}
      </div>
    `).join('');

    const links = document.getElementById('dashboard-links');
    links.innerHTML = `
      <a class="dashboard-link farmer" href="farmer_dashboard.html" onclick="return validateDashboardClick(event, 'farmer')">Farmer dashboard</a>
      <a class="dashboard-link investor" href="investors_dashboard.html" onclick="return validateDashboardClick(event, 'investor')">Investor dashboard</a>
    `;
    links.style.display = 'flex';
    const errorMessage = document.getElementById('dashboard-error');
    if (errorMessage) {
      errorMessage.style.display = 'none';
    }

    if (currentRole === 'investor') {
      document.getElementById('success-heading').innerHTML = 'Welcome,<br><em>Investor!</em>';
      document.getElementById('success-sub').textContent = 'Your investor account is ready. Start exploring farm opportunities today.';
      document.getElementById('btn-success').classList.add('inv');
    } else {
      document.getElementById('success-heading').innerHTML = 'Welcome to<br><em>AgroVest!</em>';
      document.getElementById('success-sub').textContent = 'Your farmer account is ready. Let\'s set up your farm profile.';
      document.getElementById('btn-success').classList.remove('inv');
    }

    ['dot-1','dot-2','dot-3'].forEach(id => {
      document.getElementById(id).classList.remove('active');
      document.getElementById(id).classList.add('done');
      document.getElementById(id).textContent = '✓';
    });
  }

  window.scrollTo(0, 0);
}

function goBack() {
  if (currentStep > 1) goStep(currentStep - 1);
  else window.history.back();
}

function updateProgress(step) {
  const pcts = { 1: '33%', 2: '66%', 3: '85%', 4: '100%' };
  document.getElementById('progress').style.width = pcts[step] || '33%';
}

function updateStepDots(step) {
  for (let i = 1; i <= 3; i++) {
    const d = document.getElementById('dot-' + i);
    d.classList.remove('active', 'done');
    if (i < step) d.classList.add('done');
    else if (i === step) d.classList.add('active');
  }
}

function checkStrength(val) {
  const bar  = document.getElementById('pw-bar');
  const hint = document.getElementById('pw-hint');
  let score  = 0;
  if (val.length >= 8)  score++;
  if (/[A-Z]/.test(val)) score++;
  if (/[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;

  const configs = [
    { w: '0%',   bg: 'transparent', msg: 'Use 8+ characters, a number, and a symbol' },
    { w: '25%',  bg: '#E24B4A',     msg: 'Too weak — add more characters' },
    { w: '50%',  bg: var_straw(),   msg: 'Fair — add uppercase & symbols' },
    { w: '75%',  bg: var_leaf(),    msg: 'Good — almost there!' },
    { w: '100%', bg: var_moss(),    msg: 'Strong password ✓' }
  ];
  const c = configs[score];
  bar.style.width      = c.w;
  bar.style.background = c.bg;
  hint.textContent     = c.msg;
}

function var_straw() { return '#D4A843'; }
function var_leaf()  { return '#5A8A3C'; }
function var_moss()  { return '#3B5E2B'; }

function checkTerms() {
  const checked = document.getElementById('terms').checked;
  document.getElementById('btn-step3').disabled = !checked;
}

function togglePw(inputId, iconId) {
  const el = document.getElementById(inputId);
  const ic = document.getElementById(iconId);
  if (el.type === 'password') {
    el.type = 'text';
    ic.innerHTML = `<path d="M13 6.5C11.5 4.5 9.9 3 8 3c-1.9 0-3.5 1.5-5 3.5M1 1l14 14M6.5 9.5A2 2 0 009.5 6.5" stroke-linecap="round"/>`;
  } else {
    el.type = 'password';
    ic.innerHTML = `<path d="M1 8S3.5 3 8 3s7 5 7 5-2.5 5-7 5S1 8 1 8z"/><circle cx="8" cy="8" r="2"/>`;
  }
}

function goToSelectedDashboard() {
  if (currentRole === 'farmer') {
    window.location.href = 'farmer_dashboard.html';
  } else if (currentRole === 'investor') {
    window.location.href = 'investors_dashboard.html';
  } else {
    window.location.href = 'log_in.html';
  }
}

function normalizeAccountKey(key) {
  return key.trim().replace(/[\s-]/g, '').toLowerCase();
}

function getStoredAccounts() {
  try {
    return JSON.parse(localStorage.getItem('agrovest_accounts') || '{}');
  } catch (e) {
    return {};
  }
}

function saveStoredAccounts(accounts) {
  localStorage.setItem('agrovest_accounts', JSON.stringify(accounts));
}

function submitRegistration() {
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const password = document.getElementById('pw1').value;
  const confirmPassword = document.getElementById('pw2').value;
  const firstName = document.getElementById('first-name').value.trim();
  const lastName = document.getElementById('last-name').value.trim();
  const favCrop = document.getElementById('crop').value;
  const occupation = document.getElementById('occupation').value.trim();
  const budget = document.getElementById('budget').value;

  if (!email && !phone) {
    alert('Please enter your email address or phone number.');
    goStep(2);
    return;
  }
  if (password.length < 8) {
    alert('Password must be at least 8 characters.');
    return;
  }
  if (password !== confirmPassword) {
    alert('Passwords do not match.');
    return;
  }
  if (!document.getElementById('terms').checked) {
    alert('Please agree to the terms to continue.');
    return;
  }

  const accountKey = normalizeAccountKey(email || phone);
  const accounts = getStoredAccounts();
  accounts[accountKey] = {
    role: currentRole || 'farmer',
    email,
    phone,
    password,
    firstName,
    lastName,
    farmName: document.getElementById('farm-name') ? document.getElementById('farm-name').value.trim() : '',
    crop: favCrop || '',
    occupation,
    budget
  };
  saveStoredAccounts(accounts);
  localStorage.setItem('agrovest_last_account', accountKey);
  goStep(4);
}

function validateDashboardClick(event, targetRole) {
  const errorMessage = document.getElementById('dashboard-error');
  if (currentRole !== targetRole) {
    event.preventDefault();
    if (errorMessage) {
      const roleName = currentRole === 'farmer' ? 'Farmer' : currentRole === 'investor' ? 'Investor' : 'User';
      errorMessage.textContent = `You registered as ${roleName}. Please use the ${roleName.toLowerCase()} dashboard.`;
      errorMessage.style.display = 'block';
    }
    return false;
  }
  if (errorMessage) {
    errorMessage.style.display = 'none';
  }
  return true;
}
