import type { ModelViewerElement } from '@google/model-viewer';
/** No CDN, no auto-rotation, no model/network download until an explicit click. */
const cleanups = new Set<() => void>();
function setup() {
  document.querySelectorAll<HTMLElement>('[data-medical-model]').forEach((root) => {
    if (root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const enable = root.querySelector<HTMLButtonElement>('[data-enable]')!;
    const controls = root.querySelector<HTMLElement>('[data-controls]')!;
    const viewport = root.querySelector<HTMLElement>('[data-viewport]')!;
    const status = root.querySelector<HTMLElement>('[data-status]')!;
    const slider = root.querySelector<HTMLInputElement>('[data-angle-input]');
    const output = root.querySelector<HTMLOutputElement>('[data-angle]');
    const play = root.querySelector<HTMLButtonElement>('[data-play]');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    const camera: number[] = JSON.parse(root.dataset.camera || '[0.35,0.25]');
    const closeKnee = (root.dataset.src || "").startsWith("/medical-visuals/knee-") && !(root.dataset.src || "").includes("knee-motion");
    const defaultOrbit = `${camera[0]}rad ${Math.PI / 2 - camera[1]}rad ${closeKnee ? "70%" : "105%"}`;
    let model: ModelViewerElement | undefined;
    let frame = 0;
    let destroyed = false;
    enable.hidden = false;
    const sync = () => {
      if (!model) return;
      const t = model.currentTime % 4;
      const angle = Math.round(72 * (t <= 2 ? t : 4 - t) / 2);
      if (slider) slider.value = String(angle);
      if (output) output.value = `${angle}°`;
      if (play) play.textContent = model.paused ? '播放示意動畫' : '暫停動畫';
      if (!model.paused) frame = requestAnimationFrame(sync);
    };
    const pause = () => {
      cancelAnimationFrame(frame);
      model?.pause();
      if (play) play.textContent = '播放示意動畫';
    };
    const reset = () => {
      pause(); model?.remove(); model = undefined;
      controls.hidden = true; enable.disabled = false; enable.textContent = '載入可旋轉 3D 模型';
      status.textContent = '已返回靜態圖。互動功能不影響文章閱讀。';
    };
    enable.addEventListener('click', async () => {
      if (model) { reset(); return; }
      enable.disabled = true;
      status.textContent = '正在載入 3D 模型，靜態圖仍可閱讀…';
      try {
        await import('@google/model-viewer');
        if (destroyed) return;
        model = document.createElement('model-viewer') as ModelViewerElement;
        model.setAttribute('alt', root.dataset.alt || '醫學結構示意模型');
        model.setAttribute('poster', root.dataset.poster!);
        model.setAttribute('camera-controls', '');
        model.setAttribute('interaction-prompt', 'none');
        model.setAttribute('touch-action', 'pan-y');
        model.setAttribute('shadow-intensity', '0.25');
        model.setAttribute('exposure', '0.9');
        model.setAttribute('loading', 'eager');
        model.setAttribute('camera-orbit', defaultOrbit);
        if (closeKnee) model.setAttribute('camera-target', '0m 0.018m 0.012m');
        model.setAttribute('min-camera-orbit', 'auto 10deg 35%');
        model.setAttribute('max-camera-orbit', 'auto 170deg 300%');
        if (reduce.matches) model.setAttribute('interpolation-decay', '0');
        const loaded = new Promise<void>((resolve, reject) => {
          const timer = window.setTimeout(() => reject(new Error('timeout')), 45000);
          model!.addEventListener('load', () => { clearTimeout(timer); resolve(); }, { once: true });
          model!.addEventListener('error', () => { clearTimeout(timer); reject(new Error('load')); }, { once: true });
        });
        viewport.append(model);
        model.src = root.dataset.src!;
        await loaded;
        if (destroyed || !model) return;
        model.pause(); controls.hidden = false;
        enable.disabled = false; enable.textContent = '回到靜態圖';
        status.textContent = '3D 已載入。這是簡化示意，不是診斷影像或動作評估。';
        model.addEventListener('finished', pause);
        sync();
      } catch {
        reset();
        status.textContent = '此裝置或網路暫時無法開啟 3D。請使用靜態圖、下載模型，或再次嘗試。';
      }
    });
    root.querySelectorAll<HTMLButtonElement>('[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        if (!model) return;
        const orbit = model.getCameraOrbit();
        if (button.dataset.action === 'reset') { model.cameraOrbit = defaultOrbit; model.jumpCameraToGoal(); return; }
        let theta = orbit.theta, radius = orbit.radius;
        switch (button.dataset.action) {
          case 'left': theta -= Math.PI / 12; break;
          case 'right': theta += Math.PI / 12; break;
          case 'in': radius *= .85; break;
          case 'out': radius *= 1.18; break;
        }
        model.cameraOrbit = `${theta}rad ${orbit.phi}rad ${radius}m`;
        if (reduce.matches) model.jumpCameraToGoal();
      });
    });
    slider?.addEventListener('input', () => {
      if (!model) return;
      pause(); model.currentTime = Number(slider.value) / 72 * 2;
      if (output) output.value = `${slider.value}°`;
    });
    play?.addEventListener('click', () => {
      if (!model) return;
      if (model.paused) { model.play(); sync(); }
      else pause();
    });
    const visibility = () => { if (document.hidden) pause(); };
    const reduceChanged = () => { pause(); if (model) model.setAttribute('interpolation-decay', reduce.matches ? '0' : '50'); };
    document.addEventListener('visibilitychange', visibility);
    reduce.addEventListener('change', reduceChanged);
    const observer = new IntersectionObserver((entries) => { if (!entries[0].isIntersecting) pause(); });
    observer.observe(root);
    const cleanup = () => {
      destroyed = true; reset(); observer.disconnect();
      document.removeEventListener('visibilitychange', visibility);
      reduce.removeEventListener('change', reduceChanged); cleanups.delete(cleanup);
    };
    cleanups.add(cleanup);
  });
}
setup();
document.addEventListener('astro:page-load', setup);
document.addEventListener('astro:before-swap', () => { for (const cleanup of cleanups) cleanup(); });
