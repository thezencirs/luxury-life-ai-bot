# Harvested Open-Source Motion & Video Engines (`vendor_repos`)

## 1. Vendored Reference Repository
- **Source Repository:** [`https://github.com/remotion-dev/template-overlay.git`](https://github.com/remotion-dev/template-overlay.git)
- **Local Vendored Path:** `vendor_repos/remotion-template-overlay` (shallow-cloned via `git clone --depth 1`, `.git` metadata stripped for clean deterministic vendoring)
- **Core Reference Files Inspected:**
  - `vendor_repos/remotion-template-overlay/src/Overlay.tsx` — Deterministic frame-indexed `useCurrentFrame()`, `spring()` physics solver, and `interpolate()` affine transform composition (`scale`, `translate`, `rotate`).
  - `vendor_repos/remotion-template-overlay/src/Root.tsx` — Fixed timeline `<Composition>` contract (`fps=30`, explicit frame duration, strict raster canvas bounds).

---

## 2. Mathematical Adaptation: Remotion `spring()` Physics -> 2K QHD+ Python/FFmpeg Engine

In `Overlay.tsx`, Remotion computes deterministic spring motion per frame $f \in [0, N)$ without relying on CSS non-deterministic timers:

```tsx
const scale = spring({
  fps,
  frame,
  config: { damping: 14, stiffness: 120, mass: 0.8 },
});
```

We harvest and solve the exact second-order damped harmonic oscillator differential equation in Python/NumPy for our **2K QHD+ (`1440x2560 @ 30fps`) GraphMotion Engine**:

$$m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + k (x - 1) = 0$$

Where:
- **Mass ($m$):** `0.8` (lightweight kinetic card inertia for snappy editorial entrance)
- **Stiffness ($k$):** `120.0` (high tension for crisp luxury authority)
- **Damping ($c$):** `14.0` (underdamped ratio $\zeta = \frac{c}{2\sqrt{mk}} \approx 0.714 < 1.0$, producing a subtle, physical ~3.8% luxury overshoot before settling smoothly at $1.0$)

### Closed-Form Python Solver Used in GraphMotion Bento & HUD Cards
```python
import math

def remotion_spring(frame: float, fps: float = 30.0, damping: float = 14.0, stiffness: float = 120.0, mass: float = 0.8) -> float:
    if frame <= 0:
        return 0.0
    t = frame / fps
    omega_0 = math.sqrt(stiffness / mass)
    zeta = damping / (2.0 * math.sqrt(stiffness * mass))
    if zeta < 1.0:
        omega_d = omega_0 * math.sqrt(1.0 - zeta * zeta)
        envelope = math.exp(-zeta * omega_0 * t)
        return 1.0 - envelope * (math.cos(omega_d * t) + (zeta * omega_0 / omega_d) * math.sin(omega_d * t))
    else:
        return 1.0 - (1.0 + omega_0 * t) * math.exp(-omega_0 * t)
```

---

## 3. 180-Degree Shutter Motion Blur Adaptation

Standard frame-by-frame rendering produces stroboscopic, artificial-looking motion when cards or models move rapidly across a `1440x2560` canvas. To replicate cinema cameras (Arri Alexa Mini LF / RED V-Raptor with a **180-degree rotary shutter**, i.e., $\Delta t_{\text{exposure}} = \frac{1}{2 \cdot \text{fps}} = \frac{1}{60}\text{s}$ at $30\text{ fps}$):

1. **Velocity-Vector Directional Blur (Act I & Act II Bento Cards):**
   - Instantaneous frame velocity $v_f = |x(f) - x(f - 1)|$ is derived directly from the derivative of `remotion_spring()`.
   - When $v_f > 2.0\text{ px/frame}$, directional motion sub-samples ($S = 5$ temporal sub-steps across $[f - 0.25, f + 0.25]$) are accumulated in float32 linear light before gamma encoding.
2. **FFmpeg Temporal & Mastering Pipeline:**
   - Encoded at `1440x2560`, `30 fps`, H.264 `High@L5.1`, `-crf 12`, `-b:v 22M`, `-maxrate 28M`, `-bufsize 44M`, `bt709` color primaries/transfer/matrix, ensuring zero macroblocking during high-velocity spring entrances and catwalk tracking shots.

---

## 4. Optical Camera Realism & Sensor Physics

To eliminate sterile CGI artifacts and achieve 100% editorial authenticity on `@Luxurylifeaibot`:
- **Pure White Cyclorama Studio Lighting (`#FFFFFF` -> `#F4F4F6`):** Soft-box wrap lighting with dual-layer contact shadow ($\sigma_1 = 6\text{px}$ umbra + $\sigma_2 = 28\text{px}$ ambient occlusion penumbra) anchoring every card and model footstep onto the studio floor.
- **Organic Handheld Camera Breathing:** Multi-frequency Perlin/sinusoidal micro-drift ($\Delta x(t) = A_x \sin(2\pi f_1 t) + B_x \cos(2\pi f_2 t)$, amplitude $\pm 4.5\text{px}$, angular roll $\pm 0.18^\circ$) simulating an 85mm f/1.4 prime lens held by a fashion studio DP.
- **4-Point Anisotropic Diamond & Gold Specular Glints:** Parametric cross-star diffraction kernel ($0^\circ, 90^\circ, \pm 45^\circ$ secondary rays) triggered dynamically on high-luminance metallic/gemstone pixels ($Y > 0.92$) as the light sweep crosses the item.
- **Kodak Portra 400 Silver-Halide Film Grain & Hasselblad H6D-100c Shutter Foley:** Fine monochromatic luminance grain ($\sigma_{\text{grain}} = 1.8\%$ in midtones) paired with frame-accurate mechanical leaf-shutter acoustic transients on every editorial cut.
