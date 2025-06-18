// Config
const CONFIG = {
  emulatorPath: 'emulators/emulatorJS/',
  romBasePath: 'Games/'
};

// State management
const state = {
  html5Mode: localStorage.getItem('html5Mode') || 'iframe',
  currentGame: null,
  emulator: null
};

// DOM Elements
const elements = {
  gameContainer: document.getElementById('game-container'),
  toggleBtn: document.getElementById('toggle-html5'),
  modeIndicator: document.getElementById('mode-indicator')
};

// Initialize
function init() {
  loadGameList();
  setupEventListeners();
  updateModeIndicator();
}

// Load game list from JSON
async function loadGameList() {
  try {
    const response = await fetch('game_list.json');
    const games = await response.json();
    renderGameMenu(games);
  } catch (error) {
    console.error('Failed to load game list:', error);
  }
}

// Render game menu
function renderGameMenu(games) {
  const menu = document.getElementById('game-menu');
  menu.innerHTML = '';

  games.forEach(game => {
    const gameEl = document.createElement('div');
    gameEl.className = 'game-item';
    gameEl.innerHTML = `
      <img src="${game.icon}" alt="${game.name}">
      <span>${game.name}</span>
    `;
    gameEl.addEventListener('click', () => loadGame(game));
    menu.appendChild(gameEl);
  });
}

// Core game loading function
function loadGame(game) {
  cleanupPreviousGame();
  state.currentGame = game;

  if (game.type === 'html5') {
    loadHTML5Game(game);
  } else {
    loadRomGame(game);
  }
}

// HTML5 Game Loader
function loadHTML5Game(game) {
  elements.gameContainer.innerHTML = '';

  if (state.html5Mode === 'iframe') {
    const iframe = document.createElement('iframe');
    iframe.src = game.path;
    iframe.className = 'game-frame';
    elements.gameContainer.appendChild(iframe);
  } else {
    const embed = document.createElement('embed');
    embed.src = game.path;
    embed.type = 'text/html';
    embed.className = 'game-frame';
    elements.gameContainer.appendChild(embed);
  }
}

// ROM Loader with EmulatorJS
function loadRomGame(game) {
  elements.gameContainer.innerHTML = `
    <div id="emulator-container">
      <canvas id="emulator-canvas"></canvas>
      <div class="emulator-controls"></div>
    </div>
  `;

  // Dynamic script loading
  const script = document.createElement('script');
  script.src = `${CONFIG.emulatorPath}emulator.js`;
  document.head.appendChild(script);

  script.onload = () => {
    initEmulator(game);
  };
}

// Initialize EmulatorJS
function initEmulator(game) {
  const canvas = document.getElementById('emulator-canvas');
  const fullPath = `${CONFIG.romBasePath}${game.path}`;

  state.emulator = new EmulatorJS({
    canvas: canvas,
    core: game.core,
    dataPath: `${CONFIG.emulatorPath}data/`,
    libPath: `${CONFIG.emulatorPath}lib/`,
    biosPath: `${CONFIG.emulatorPath}bios/`,
    workerPath: `${CONFIG.emulatorPath}worker/`,
    rom: fullPath
  });

  state.emulator.start();
}

// Toggle between iframe/embed
function toggleHTML5Mode() {
  state.html5Mode = state.html5Mode === 'iframe' ? 'embed' : 'iframe';
  localStorage.setItem('html5Mode', state.html5Mode);
  updateModeIndicator();
  
  // Reload current game if HTML5
  if (state.currentGame?.type === 'html5') {
    loadGame(state.currentGame);
  }
}

// Cleanup previous game
function cleanupPreviousGame() {
  if (state.emulator) {
    state.emulator.stop();
    state.emulator = null;
  }
  elements.gameContainer.innerHTML = '';
}

// Update UI indicator
function updateModeIndicator() {
  elements.modeIndicator.textContent = `HTML5 Mode: ${state.html5Mode.toUpperCase()}`;
}

// Event listeners
function setupEventListeners() {
  elements.toggleBtn.addEventListener('click', toggleHTML5Mode);
}

// Initialize loader
window.addEventListener('DOMContentLoaded', init);
