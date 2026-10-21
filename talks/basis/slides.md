---
theme: default
author: Kai Ye
routerMode: hash
transition: slide-left
colorSchema: light
fonts:
  provider: none
drawings:
  persist: false
aspectRatio: 1.7777777777777777
info: |
  BASIS research talk, converted from the original PowerPoint.
layout: none
class: bg-white
title: "BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning"
---

<img src="/slides/slide-01.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 1: BASIS" />

<div class="sr-only">
  <h1>BASIS</h1>
  <p>RESEARCH TALK</p>
  <p>BASIS:</p>
  <p>Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning</p>
  <p>Kai Ye</p>
  <p>Department of Statistics, LSE &amp; Stats-Powered AI Lab</p>
  <p>BASIS</p>
  <p>1</p>
</div>

---
layout: none
class: bg-white
title: "Roadmap"
---

<img src="/slides/slide-02.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 2: Roadmap" />

<div class="sr-only">
  <h1>Roadmap</h1>
  <p>OVERVIEW</p>
  <p>Roadmap</p>
  <p>This talk is organized around four questions.</p>
  <p>01</p>
  <p>What is the optimization problem?</p>
  <p>02</p>
  <p>What is the drawback of PPO and GRPO</p>
  <p>03</p>
  <p>What exactly is BASIS?</p>
  <p>04</p>
  <p>How does BASIS perform?</p>
  <p>The central advantage of BASIS</p>
  <p>No value model needed</p>
  <p>Better than PPO</p>
  <p>Works with A Single Sample</p>
  <p>Better than GRPO</p>
  <p>Shares inter-query information</p>
  <p>Lower baseline variance</p>
  <p>BASIS</p>
  <p>2</p>
</div>

---
layout: none
class: bg-white
title: "Background: Large Language Model reasoning and training"
---

<img src="/slides/slide-03.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 3: Background: Large Language Model reasoning and training" />

<div class="sr-only">
  <h1>Background: Large Language Model reasoning and training</h1>
  <p>OVERVIEW</p>
  <p>Background</p>
  <p>METHOD DETAIL</p>
  <p>Large Language Model reasoning and training</p>
  <p>BASIS</p>
  <p>3</p>
</div>

---
layout: none
class: bg-white
title: "Background: Large Language Model reasoning"
---

<img src="/slides/slide-04.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 4: Background: Large Language Model reasoning" />

<div class="sr-only">
  <h1>Background: Large Language Model reasoning</h1>
  <p>MOTIVATION</p>
  <p>Background</p>
  <p>Large Language Model reasoning</p>
  <p>Prompt</p>
  <p>x ∼ D</p>
  <p>Policy</p>
  <p>πθ(·|x)</p>
  <p>Reasoning</p>
  <p>c</p>
  <p>Step 1 analysis: To solve ….“Half the value of 3x - 9 is x + 37” means: (1/2)(3x - 9) = x + 37</p>
  <p>Step 2 calculation: To eliminate … 2:3x - 9 = 2(x + 37)</p>
  <p>Next, we distribute … 3x - 9 = 2x + 74. Now, we … x - 9 = 74</p>
  <p>Finally, we add … x = 83</p>
  <p>Step 3 verification: Let&#x27;s verify … x = 83 … the left side … right side …120, confirming that our solution is correct.</p>
  <p>Final Answer: Therefore, the value of x is 83.</p>
  <p>Question:</p>
  <p>Half the value of 3x-9 is x+37. What is the value of x?</p>
  <p>Prompt</p>
  <p>Reasoning Steps</p>
  <p>Final Answer</p>
  <p>Answer</p>
  <p>y</p>
  <p>Reward</p>
  <p>r(x,y)</p>
  <p>BASIS</p>
  <p>4</p>
</div>

---
layout: none
class: bg-white
title: "Background: Reinforcement Learning"
---

<img src="/slides/slide-05.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 5: Background: Reinforcement Learning" />

<div class="sr-only">
  <h1>Background: Reinforcement Learning</h1>
  <p>OVERVIEW</p>
  <p>Background</p>
  <p>METHOD DETAIL</p>
  <p>Reinforcement Learning</p>
  <p>BASIS</p>
  <p>5</p>
</div>

---
layout: none
class: bg-white
title: "Baseline 1"
---

<img src="/slides/slide-06.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 6: Baseline 1" />

<div class="sr-only">
  <h1>Baseline 1</h1>
  <p>MOTIVATION</p>
  <p>Baseline 1</p>
  <p>Gradient high variance！</p>
  <p>Possible solution：Subtract a baseline term</p>
  <p>A function of random variable X</p>
  <p>Conditionally independent of Y and R given X</p>
  <p>Unbiased</p>
  <p>Reduce the variance of the estimator</p>
  <p>BASIS</p>
  <p>6</p>
</div>

---
layout: none
class: bg-white
title: "Baseline 2"
---

<img src="/slides/slide-07.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 7: Baseline 2" />

<div class="sr-only">
  <h1>Baseline 2</h1>
  <p>MOTIVATION</p>
  <p>Baseline 2</p>
  <p>One sample is needed</p>
  <p>A separate value model is needed</p>
  <p>BASIS</p>
  <p>7</p>
</div>

---
layout: none
class: bg-white
title: "Baseline 3"
---

<img src="/slides/slide-08.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 8: Baseline 3" />

<div class="sr-only">
  <h1>Baseline 3</h1>
  <p>MOTIVATION</p>
  <p>Baseline 3</p>
  <p>No separate value model is needed</p>
  <p>A group of sample is needed</p>
  <p>BASIS</p>
  <p>8</p>
</div>

---
layout: none
class: bg-white
title: "PPO versus GRPO"
---

<img src="/slides/slide-09.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 9: PPO versus GRPO" />

<div class="sr-only">
  <h1>PPO versus GRPO</h1>
  <p>BACKGROUND</p>
  <p>PPO versus GRPO</p>
  <p>Method</p>
  <p>Value model</p>
  <p>Needs G&gt;1</p>
  <p>Cross-prompt info</p>
  <p>PPO</p>
  <p>Yes</p>
  <p>No</p>
  <p>No</p>
  <p>GRPO</p>
  <p>No</p>
  <p>Usually yes</p>
  <p>No</p>
  <p>BASIS</p>
  <p>No</p>
  <p>No</p>
  <p>Yes</p>
  <p>PPO</p>
  <p>Stable and effective even with one sampled completion per prompt.</p>
  <p>But advantage estimation typically requires a separate value model.</p>
  <p>GRPO</p>
  <p>Avoids value fitting by using within-prompt group statistics.</p>
  <p>But local group normalization becomes fragile when G is small.</p>
  <p>BASIS</p>
  <p>9</p>
</div>

---
layout: none
class: bg-white
title: "Core intuition"
---

<img src="/slides/slide-10.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 10: Core intuition" />

<div class="sr-only">
  <h1>Core intuition</h1>
  <p>BAS</p>
  <p>Core intuition</p>
  <p>Current limitation.</p>
  <p>Different prompts in the same mini-batch are usually treated as independent training units.</p>
  <p>Key observation.</p>
  <p>However, prompts may share latent information, such as difficulty level, solution structure, and reward behavior, rather than being completely unrelated.</p>
  <p>Mini-batch as a graph</p>
  <p>x1</p>
  <p>x2</p>
  <p>x3</p>
  <p>x4</p>
  <p>x5</p>
  <p>x6</p>
  <p>BASIS uses the training-batch as a statistical neighborhood.</p>
  <p>METHOD DETAIL</p>
  <p>BASIS</p>
  <p>10</p>
</div>

---
layout: none
class: bg-white
title: "BASIS: Batchwise Advantage"
---

<img src="/slides/slide-11.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 11: BASIS: Batchwise Advantage" />

<div class="sr-only">
  <h1>BASIS: Batchwise Advantage</h1>
  <p>BASIS: Batchwise Advantage</p>
  <p>From local groups to batchwise information sharing</p>
  <p>The update rule remains familiar; the baseline estimator is what changes.</p>
  <p>BASIS</p>
  <p>11</p>
</div>

---
layout: none
class: bg-white
title: "Single-rollout effective (even using half time)"
---

<img src="/slides/slide-12.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 12: Single-rollout effective (even using half time)" />

<div class="sr-only">
  <h1>Single-rollout effective (even using half time)</h1>
  <p>THEORY</p>
  <p>Single-rollout effective (even using half time)</p>
  <p>Experiments</p>
  <p>BASIS</p>
  <p>12</p>
</div>

---
layout: none
class: bg-white
title: "Two key questions"
---

<img src="/slides/slide-13.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 13: Two key questions" />

<div class="sr-only">
  <h1>Two key questions</h1>
  <p>BAS</p>
  <p>Two key questions</p>
  <p>How can we define and quantify such shared information?</p>
  <p>METHOD DETAIL</p>
  <p>How can this information be used to help prompts learn from each other?</p>
  <p>BASIS</p>
  <p>13</p>
</div>

---
layout: none
class: bg-white
title: "Our Initial Goal"
---

<img src="/slides/slide-14.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 14: Our Initial Goal" />

<div class="sr-only">
  <h1>Our Initial Goal</h1>
  <p>BAS</p>
  <p>Our Initial Goal</p>
  <p>V𝑖𝑡=ℎ∈ℬ𝓉𝐾𝑡𝑥𝑖,𝑥ℎ 𝜇ℎ𝑡.</p>
  <p>𝐾𝑡𝑥𝑖,𝑥ℎ is a batch-dependent cross-prompt information borrowing coefficient, measuring how much the empirical reward statistic from prompt 𝑥ℎ contributes to the baseline estimate for prompt 𝑥𝑖at training step (𝑡)</p>
  <p>Find a good 𝐾𝑡𝑥𝑖,𝑥ℎ in :</p>
  <p>METHOD DETAIL</p>
  <p>BASIS</p>
  <p>14</p>
</div>

---
layout: none
class: bg-white
title: "Batchwise refinement: Proposition 1 (BLUE)"
---

<img src="/slides/slide-15.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 15: Batchwise refinement: Proposition 1 (BLUE)" />

<div class="sr-only">
  <h1>Batchwise refinement: Proposition 1 (BLUE)</h1>
  <p>BAS</p>
  <p>Batchwise refinement: Proposition 1 (BLUE)</p>
  <p>V𝑘=𝑗=1𝐽𝑤𝑗𝜇𝑗, such that 𝔼V𝑘=𝜇𝑘,</p>
  <p>𝑤𝑗=𝜇𝑘 𝜇𝑗/𝜎𝑗2ℓ=1𝐽𝜇ℓ2/𝜎ℓ2.</p>
  <p>The constrained MSE-minimizing linear unbiased estimator of 𝜇𝑘,</p>
  <p>Can be found has best linear unbiased estimator (BLUE)</p>
  <p>How can we get access to  𝜇𝑘 in our online training?</p>
  <p>METHOD DETAIL</p>
  <p>BASIS</p>
  <p>15</p>
</div>

---
layout: none
class: bg-white
title: "Offline prompt signal: Proposition 2 (Closed-form value)"
---

<img src="/slides/slide-16.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 16: Offline prompt signal: Proposition 2 (Closed-form value)" />

<div class="sr-only">
  <h1>Offline prompt signal: Proposition 2 (Closed-form value)</h1>
  <p>Offline prompt signal: Proposition 2 (Closed-form value under 𝝅𝜷∗)</p>
  <p>Why this is useful</p>
  <p>It approximates the Value form KL-regularized oracle value.</p>
  <p>The same offline cache can support different training stages by changing β.</p>
  <p>Changing β does not require recollecting data.</p>
  <p>Hence the signal is practical and reusable.</p>
  <p>𝑉𝛽∗𝑥:=𝔼𝑦∼𝜋𝛽∗⋅∣𝑥𝑟(𝑥,𝑦)</p>
  <p>This is the closed form value under  𝜋𝛽∗</p>
  <p>and is derivd from optimal value of the 𝛽-KL-regularized objective</p>
  <p>𝑉𝛽∗𝑥=𝔼𝑦∼𝜋ref⋅∣𝑥 𝑟(𝑥,𝑦)exp𝑟(𝑥,𝑦)𝛽𝔼𝑦∼𝜋ref⋅∣𝑥 exp𝑟(𝑥,𝑦)𝛽</p>
  <p>𝑉𝛽⋆𝑥’=sup𝜋𝔼𝑌∼𝜋⋅∣𝑥𝑟(𝑥,𝑦)−𝛽 KL 𝜋⋅∣𝑥∥𝜋ref⋅∣𝑥</p>
  <p>BAS</p>
  <p>METHOD DETAIL</p>
  <p>BASIS</p>
  <p>16</p>
</div>

---
layout: none
class: bg-white
title: "Online calibration: How to select beta during online training?"
---

<img src="/slides/slide-17.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 17: Online calibration: How to select beta during online training?" />

<div class="sr-only">
  <h1>Online calibration: How to select beta during online training?</h1>
  <p>METHOD DETAIL</p>
  <p>Online calibration: How to select 𝜷 during online training?</p>
  <p>𝛽𝑡∈argmin𝛽∈𝔹1ℬ𝓉𝑖∈ℬ𝓉(𝜇𝑖𝑡−𝑉𝑖,𝑡,𝛽)2</p>
  <p>high (early)</p>
  <p>low (late)</p>
  <p>𝛽𝑡</p>
  <p>Converged</p>
  <p>(KL dominates)</p>
  <p>β → ∞</p>
  <p>β = 0</p>
  <p>(KL vanishes)</p>
  <p>Start</p>
  <p>BASIS</p>
  <p>17</p>
</div>

---
layout: none
class: bg-white
title: "Batchwise baseline"
---

<img src="/slides/slide-18.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 18: Batchwise baseline" />

<div class="sr-only">
  <h1>Batchwise baseline</h1>
  <p>METHOD DETAIL</p>
  <p>Batchwise baseline</p>
  <p>𝐾𝑡𝑥𝑖,𝑥ℎ=𝑉𝛽𝑡𝑥𝑖 𝑉𝛽𝑡𝑥ℎ𝑢∈ℬ𝓉𝑉𝛽𝑡𝑥𝑢2,  𝑖,ℎ∈ℬ𝓉.</p>
  <p>V𝑖𝑡=𝑉𝛽𝑡𝑥𝑖 ℎ∈ℬ𝓉𝑉𝛽𝑡𝑥ℎ 𝜇ℎ𝑡𝑢∈ℬ𝓉𝑉𝛽𝑡𝑥𝑢2.</p>
  <p>Cross-prompt information borrowing coefficient:</p>
  <p>Baseline:</p>
  <p>BASIS</p>
  <p>18</p>
</div>

---
layout: none
class: bg-white
title: "Interpretation"
---

<img src="/slides/slide-19.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 19: Interpretation" />

<div class="sr-only">
  <h1>Interpretation</h1>
  <p>METHOD DETAIL</p>
  <p>Interpretation</p>
  <p>V𝑖𝑡=𝑉𝛽𝑡𝑥𝑖 ℎ∈ℬ𝓉𝑉𝛽𝑡𝑥ℎ 𝜇ℎ𝑡𝑢∈ℬ𝓉𝑉𝛽𝑡𝑥𝑢2.</p>
  <p>V𝑖𝑡=ℎ∈ℬ𝓉𝑉𝛽𝑡𝑥ℎ2𝑢∈ℬ𝓉𝑉𝛽𝑡𝑥𝑢2𝑉𝛽𝑡𝑥𝑖𝑉𝛽𝑡𝑥ℎ𝜇ℎ𝑡.</p>
  <p>Each prompt carries its own notion of difficulty, quality, or latent reward level.</p>
  <p>The offline value signal 𝑉𝛽𝑥𝑖 provides a compact summary of this prompt-level structure.</p>
  <p>We use this offline value signal to define similarity between prompts。</p>
  <p>Difficulty rescaling</p>
  <p>Remove the difficulty scale from the reward behavior observed at 𝑥ℎ.</p>
  <p>Rescale it to the difficulty level of 𝑥𝑖.</p>
  <p>Confidence weight</p>
  <p>Larger offline value signal has higher leverage</p>
  <p>BASIS</p>
  <p>19</p>
</div>

---
layout: none
class: bg-white
title: "Method overview"
---

<img src="/slides/slide-20.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 20: Method overview" />

<div class="sr-only">
  <h1>Method overview</h1>
  <p>Method overview</p>
  <p>7</p>
  <p>METHOD DETAIL</p>
  <p>BASIS</p>
  <p>20</p>
</div>

---
layout: none
class: bg-white
title: "Experiments"
---

<img src="/slides/slide-21.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 21: Experiments" />

<div class="sr-only">
  <h1>Experiments</h1>
  <p>Experiments</p>
  <p>BAS helps for two complementary reasons:</p>
  <p>lower variance</p>
  <p>better preservation of learning signal.</p>
  <p>BASIS</p>
  <p>21</p>
</div>

---
layout: none
class: bg-white
title: "Single-rollout effective (even using half time)"
---

<img src="/slides/slide-22.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 22: Single-rollout effective (even using half time)" />

<div class="sr-only">
  <h1>Single-rollout effective (even using half time)</h1>
  <p>THEORY</p>
  <p>Single-rollout effective (even using half time)</p>
  <p>Experiments</p>
  <p>BASIS</p>
  <p>22</p>
</div>

---
layout: none
class: bg-white
title: "BASIS is robust and informative"
---

<img src="/slides/slide-23.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 23: BASIS is robust and informative" />

<div class="sr-only">
  <h1>BASIS is robust and informative</h1>
  <p>THEORY</p>
  <p>BASIS is robust and informative</p>
  <p>GRPO have high variance when the question is medium and gradient collapse when question is easy or difficult</p>
  <p>Experiments</p>
  <p>BASIS</p>
  <p>23</p>
</div>

---
layout: none
class: bg-white
title: "BASIS is sample efficient and robust"
---

<img src="/slides/slide-24.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 24: BASIS is sample efficient and robust" />

<div class="sr-only">
  <h1>BASIS is sample efficient and robust</h1>
  <p>Experiments</p>
  <p>BASIS is sample efficient and robust</p>
  <p>BASIS has smaller MSE with single-rollout and robustness to within-batch reward heterogeneity</p>
  <p>BASIS</p>
  <p>24</p>
</div>

---
layout: none
class: bg-white
title: "Summary"
---

<img src="/slides/slide-25.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 25: Summary" />

<div class="sr-only">
  <h1>Summary</h1>
  <p>PRACTICE</p>
  <p>Summary</p>
  <p>Batchwise Advantage Shaping</p>
  <p>14</p>
  <p>Method</p>
  <p>Value model</p>
  <p>Needs G&gt;1</p>
  <p>Cross-prompt info</p>
  <p>PPO</p>
  <p>Yes</p>
  <p>No</p>
  <p>No</p>
  <p>GRPO</p>
  <p>No</p>
  <p>Usually yes</p>
  <p>No</p>
  <p>BASIS</p>
  <p>No</p>
  <p>No</p>
  <p>Yes</p>
  <p>Single-sample regime</p>
  <p>When G = 1, vanilla GRPO becomes fragile, but BASIS can still borrow along the prompt dimension.</p>
  <p>Systems appeal</p>
  <p>No extra value model to train, store, or synchronize.</p>
  <p>Potentially lower inference cost than large-group GRPO.</p>
  <p>Use cases</p>
  <p>RLVR with verifiable rewards.</p>
  <p>Reasoning, mathematics, code, and other structured tasks.</p>
  <p>BASIS</p>
  <p>25</p>
</div>
