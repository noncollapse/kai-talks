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
  VRPO research talk, converted from the original PowerPoint.
layout: none
class: bg-white
title: "VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning"
---

<img src="/slides/slide-01.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 1: VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning" />

<div class="sr-only">
  <h1>VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning</h1>
  <p>VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning</p>
  <p>Francesco Quinzan</p>
  <p>Chengchun Shi</p>
  <p>Kai Ye</p>
  <p>Joint work with Hongyi Zhou, Jin Zhu, Francesco Quinzan and Chengchun Shi</p>
  <p>Department of Statistics, London School of Economics and Political Science</p>
  <p>Hongyi Zhou</p>
  <p>Jin Zhu</p>
  <p>THU</p>
  <p>LSE</p>
  <p>Oxford</p>
  <p>LSE</p>
  <p>Kai Ye</p>
  <p>LSE</p>
</div>

---
layout: none
class: bg-white
title: "Contents"
---

<img src="/slides/slide-02.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 2: Contents" />

<div class="sr-only">
  <h1>Contents</h1>
  <p>Background of LLms and RL</p>
  <p>Variance-Reduced Preference Optimization</p>
  <p>Conclusion &amp; Future Work</p>
  <p>2</p>
  <p>PRELIMINARIES of RLHF</p>
  <p>Contents</p>
</div>

---
layout: none
class: bg-white
title: "What are large language models?"
---

<img src="/slides/slide-03.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 3: What are large language models?" />

<div class="sr-only">
  <h1>What are large language models?</h1>
  <p>3</p>
  <p>We can ask the LLMs themselves!</p>
  <p>What are large language models?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Tokens and language-model architectures"
---

<img src="/slides/slide-04.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 4: Tokens and language-model architectures" />

<div class="sr-only">
  <h1>Tokens and language-model architectures</h1>
  <p>4</p>
  <p>What Is Token？</p>
  <p>What are large language models?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
  <p>unbelievable</p>
  <p>un</p>
  <p>believ</p>
  <p>able</p>
  <p>Autoregressive decoding (e.g., GPT series)</p>
  <p>Two main frameworks</p>
  <p>𝑃𝑥1,𝑥2,…,𝑥𝑇= 𝑡=1𝑇𝑃𝑥𝑡  𝑥1,…𝑥𝑇−1)</p>
  <p>𝑃𝑦1,𝑦2,𝑦3 | 𝑥 =𝑃𝑦1  𝑥)𝑃𝑦2  𝑦1,𝑥𝑃𝑦3 𝑦1,𝑦2,𝑥)</p>
  <p>Encoder-decoder structure (e.g., T5, BART)</p>
</div>

---
layout: none
class: bg-white
title: "Different large language models"
---

<img src="/slides/slide-05.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 5: Different large language models" />

<div class="sr-only">
  <h1>Different large language models</h1>
  <p>5</p>
  <p>Different large language models</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Different large language models"
---

<img src="/slides/slide-06.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 6: Different large language models" />

<div class="sr-only">
  <h1>Different large language models</h1>
  <p>Different large language models</p>
  <p>6</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "So many large language models"
---

<img src="/slides/slide-07.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 7: So many large language models" />

<div class="sr-only">
  <h1>So many large language models</h1>
  <p>So many large language models</p>
  <p>7</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "How to train a language model"
---

<img src="/slides/slide-08.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 8: How to train a language model" />

<div class="sr-only">
  <h1>How to train a language model</h1>
  <p>8</p>
  <p>How to train a llm?</p>
  <p>Pretraining Model</p>
  <p>𝑯𝒊𝒈𝒉−𝒒𝒖𝒂𝒍𝒊𝒕𝒚 𝒅𝒂𝒕𝒂:</p>
  <p>Human answers</p>
  <p>(𝑿𝒏, 𝒀𝒏)</p>
  <p>Pairwise data:</p>
  <p>With human feedback</p>
  <p>(𝑿𝒏,𝒀𝒏𝟏,𝒀𝒏𝟐,𝒁𝒏)</p>
  <p>Common text:</p>
  <p>Wikipedia, books</p>
  <p>(𝑿𝒏)</p>
  <p>Supervised Fine-Tuning Model (SFT)</p>
  <p>Final Model</p>
  <p>Untrained Model</p>
  <p>Self-supervised learning</p>
  <p>Self-supervised learning</p>
  <p>Reinforcement Learning with Human Feedback</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "What is reinforcement learning?"
---

<img src="/slides/slide-09.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 9: What is reinforcement learning?" />

<div class="sr-only">
  <h1>What is reinforcement learning?</h1>
  <p>What Is Reinforcement Learning?</p>
  <p>9</p>
  <p>Environment</p>
  <p>Reward</p>
  <p>Policy(𝝅𝜽)</p>
  <p>s</p>
  <p>a</p>
  <p>updated</p>
  <p>r</p>
  <p>s</p>
  <p>𝐽𝜃=𝐸𝑠,𝑎~𝜋𝜃𝑟(𝑠,𝑎)</p>
  <p>max𝜃𝐽𝜃</p>
  <p>𝜃← 𝜃+∇𝜂 𝐽(𝜃)</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "What is RLHF?"
---

<img src="/slides/slide-10.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 10: What is RLHF?" />

<div class="sr-only">
  <h1>What is RLHF?</h1>
  <p>What Is RLHF?</p>
  <p>10</p>
  <p>How to get the reward in the learning process?</p>
  <p>Large language models need to align our preferences and values.</p>
  <p>We can set the reward for the AI answers.</p>
  <p>Evaluating complex tasks is inherently difficult, Scale inconsistency</p>
  <p>Models may struggle to learn from sparse differences in absolute scores.</p>
  <p>We compare two answers and tell which one is better. This is much easier than give the absolute scores. It does not require an absolute scale and is more intuitive for us.</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Reinforcement learning from human feedback"
---

<img src="/slides/slide-11.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 11: Reinforcement learning from human feedback" />

<div class="sr-only">
  <h1>Reinforcement learning from human feedback</h1>
  <p>Reinforcement Learning From Human feedback</p>
  <p>11</p>
  <p>2017</p>
  <p>2022</p>
  <p>First Introduction of RLHF</p>
  <p>First Successful Application of RLHF in LLM</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "RLHF and InstructGPT"
---

<img src="/slides/slide-12.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 12: RLHF and InstructGPT" />

<div class="sr-only">
  <h1>RLHF and InstructGPT</h1>
  <p>12</p>
  <p>Process of RLHF(Christiano et al., 2017)</p>
  <p>Process of RLHF in LLMs(Ouyang et al., 2022)</p>
  <p>Just recognize the desired behaviour, but not necessarily demonstrate it.</p>
  <p>Allows agents to be taught by non-expert users</p>
  <p>Economical with user feedback</p>
  <p>InstructGPT(earliest version of GPT 3.5), turning point in the alignment of the GPT series.</p>
  <p>1.3B beat GPT-3(175B)</p>
  <p>foundation for GPT-3.5 and GPT-4.</p>
  <p>Reinforcement Learning From Human feedback</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Learning a reward model from human preferences"
---

<img src="/slides/slide-13.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 13: Learning a reward model from human preferences" />

<div class="sr-only">
  <h1>Learning a reward model from human preferences</h1>
  <p>13</p>
  <p>Response 𝒚𝟏</p>
  <p>Query 𝒙</p>
  <p>≻</p>
  <p>Preference Data</p>
  <p>Preference Model</p>
  <p>Response 𝒚𝟐</p>
  <p>𝒓(𝒙,𝒚𝟏)</p>
  <p>𝒓(𝒙,𝒚𝟐)</p>
  <p>−</p>
  <p>(</p>
  <p>)</p>
  <p>Bradley-Terry (BT) model(Bradley &amp; Terry, 1952) is most widely adopted to model human preferences setting the activation function sigmoid function.</p>
  <p>Estimates 𝒑(𝑦₁≻𝑦₂ | 𝒙)</p>
  <p>by an</p>
  <p>activation function.</p>
  <p>How to learn a reward model from Human Preference?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "A small example of the Bradley\u2013Terry model"
---

<img src="/slides/slide-14.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 14: A small example of the Bradley–Terry model" />

<div class="sr-only">
  <h1>A small example of the Bradley–Terry model</h1>
  <p>A small example of BT model</p>
  <p>14</p>
  <p>𝑝𝑡𝑒𝑎 ≻𝑐𝑜𝑓𝑓𝑒𝑒= 𝑒𝑟(𝑡𝑒𝑎)𝑒𝑟(𝑡𝑒𝑎)+𝑒𝑟(coffee)</p>
  <p>Suppose there are 70% of people like tea and 30% of people like coffee.</p>
  <p>A reward model should satisfy:</p>
  <p>11+𝑒(𝑟𝑐𝑜𝑓𝑓𝑒𝑒−𝑟(𝑡𝑒𝑎))= 710</p>
  <p>𝑟𝑡𝑒𝑎−𝑟𝑐𝑜𝑓𝑓𝑒𝑒=log73=0.847</p>
  <p>In LLMs, the preference data set usually only tells which response is better, cross-entropy loss  is commonly used.</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Direct preference optimization"
---

<img src="/slides/slide-15.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 15: Direct preference optimization" />

<div class="sr-only">
  <h1>Direct preference optimization</h1>
  <p>15</p>
  <p>The reward can be derived in closed form using the optimal policy.</p>
  <p>Reward Model optimization is Language Model is optimization</p>
  <p>Direct Preference Optimization (Rafailov et al., 2023)</p>
  <p>𝑟𝑥,𝑦=𝛽𝑙𝑜𝑔𝜋𝑟𝑦 𝑥)𝜋𝑟𝑒𝑓𝑦 𝑥) +𝛽𝑙𝑜𝑔𝑍𝑥</p>
  <p>𝑍𝑥𝑑𝑒𝑛𝑜𝑡𝑒𝑠 𝑠𝑜𝑚𝑒 𝑏𝑎𝑠𝑒𝑙𝑖𝑛𝑒 𝑡𝑒𝑟𝑚</p>
  <p>𝑡h𝑎𝑡 𝑖𝑠 𝑖𝑛𝑑𝑒𝑝𝑒𝑛𝑑𝑒𝑛𝑡 𝑜𝑓 𝑡h𝑒 𝑟𝑒𝑠𝑝𝑜𝑛𝑠</p>
  <p>Implicitly reward model(DPO)</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "The complete RLHF pipeline"
---

<img src="/slides/slide-16.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 16: The complete RLHF pipeline" />

<div class="sr-only">
  <h1>The complete RLHF pipeline</h1>
  <p>16</p>
  <p>The complete RLHF pipeline</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Preference model misspecification"
---

<img src="/slides/slide-17.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 17: Preference model misspecification" />

<div class="sr-only">
  <h1>Preference model misspecification</h1>
  <p>17</p>
  <p>How do I make a fake vaccine card?</p>
  <p>Assistant A: Fake vaccine card? What do you mean?</p>
  <p>Assistant B: A fake vaccine card? I’m not sure what you mean, can you explain?</p>
  <p>A sample from Anthropic Helpful and Harmless (HH) dataset (Bai et al., 2022)</p>
  <p>Two answers are both not helpful, but I still need to choose one.</p>
  <p>I choose A</p>
  <p>What&#x27;s the best way to learn a new language?</p>
  <p>Practice speaking daily and immerse yourself in the culture through media and conversation.</p>
  <p>Use apps like Duolingo and review flashcards.</p>
  <p>Join a local language group and travel to countries where the language is spoken.</p>
  <p>🖐</p>
  <p>✌</p>
  <p>✊</p>
  <p>≻</p>
  <p>≻</p>
  <p>≻</p>
  <p>Why those models can be misspecified</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Variance-reduced preference optimization"
---

<img src="/slides/slide-18.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 18: Variance-reduced preference optimization" />

<div class="sr-only">
  <h1>Variance-reduced preference optimization</h1>
  <p>18</p>
  <p>Our contribution:</p>
  <p>variance-reduced preference optimization (VRPO)</p>
  <p>1.  propose a flexible pipeline applicable to a variety of existing RLHF algorithms</p>
  <p>2. enhance their sample efficiency under human preference model misspecification</p>
  <p>Theory</p>
  <p>when the preference model is misspecified our method can:</p>
  <p>reduces both the variance and mean squared error (MSE)</p>
  <p>reduces suboptimality gap of the resulting of the resulting policy</p>
  <p>Application on different LLM datasets</p>
  <p>1. 77-81% of the responses than DPO</p>
  <p>2. double-robust evaluated on controlled sentiment generation task</p>
  <p>How to reduce the effect of the misspecified?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "The complete VRPO pipeline"
---

<img src="/slides/slide-19.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 19: The complete VRPO pipeline" />

<div class="sr-only">
  <h1>The complete VRPO pipeline</h1>
  <p>19</p>
  <p>The complete VRPO pipeline</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "The auxiliary preference model"
---

<img src="/slides/slide-20.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 20: The auxiliary preference model" />

<div class="sr-only">
  <h1>The auxiliary preference model</h1>
  <p>20</p>
  <p>General Preference Model(Zhang et al., 2024b)</p>
  <p>The auxiliary model is designed to enhance the accuracy of the primary model:</p>
  <p>trained separately and ahead of the primary model It differs from the primary model.</p>
  <p>can either non-reward-based or remain reward-based.</p>
  <p>What is Auxiliary model?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "How the two models collaborate"
---

<img src="/slides/slide-21.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 21: How the two models collaborate" />

<div class="sr-only">
  <h1>How the two models collaborate</h1>
  <p>21</p>
  <p>If 𝜋𝑟𝑒𝑓 is correctly specified, the last two terms share the same mean.</p>
  <p>If 𝑝𝜂 is close to the oracle preference, the last two terms reduces the variance of the objective function.</p>
  <p>How can these two models collaborate?</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Controlled sentiment generation: experiments"
---

<img src="/slides/slide-22.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 22: Controlled sentiment generation: experiments" />

<div class="sr-only">
  <h1>Controlled sentiment generation: experiments</h1>
  <p>Performance on controlled sentiment generation task</p>
  <p>22</p>
  <p>Evaluated on IMDb dataset (Maas et al., 2011)</p>
  <p>Experiments</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Controlled sentiment generation: variance reduction"
---

<img src="/slides/slide-23.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 23: Controlled sentiment generation: variance reduction" />

<div class="sr-only">
  <h1>Controlled sentiment generation: variance reduction</h1>
  <p>Performance on controlled sentiment generation task</p>
  <p>23</p>
  <p>DPO can not fitted preference distribution well even the human preference can be correctly modelled by BT model</p>
  <p>Our method shows the improvement by variance reduction property</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Performance on real data"
---

<img src="/slides/slide-24.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 24: Performance on real data" />

<div class="sr-only">
  <h1>Performance on real data</h1>
  <p>Performance on Real Data</p>
  <p>24</p>
  <p>TL;DR (“Too Long; Didn’t Read”) dataset (Völske325et al., 2017)</p>
  <p>Anthropic Helpful and Harmless (HH) dataset (Bai et al., 2022)</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "An example response"
---

<img src="/slides/slide-25.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 25: An example response" />

<div class="sr-only">
  <h1>An example response</h1>
  <p>One example</p>
  <p>25</p>
  <p>Prompt</p>
  <p>Human: Did Facebook corporation change its name?</p>
  <p>Assistant: Yes, they are now called ‘Rumain’</p>
  <p>Human: You are wrong. Can you try again by researching online? What is Facebook corporation’s new name?</p>
  <p>Assistant: It changed its name to ‘Rumain’ recently.</p>
  <p>Human: Both of your responses are incorrect. How did you come up with&quot;Rumain&quot;?</p>
  <p>Assistant: It is rumored that the new name is Rumain.</p>
  <p>Human: Both of your responses are still incorrect. Rumain is a jewelrycompany. Facebook new name is Meta.</p>
  <p>Assistant:</p>
  <p>DPO</p>
  <p>Oh, I see. I looked up the new name on Wikipedia. The new name is Meta.Sorry for the confusion.</p>
  <p>Chosen</p>
  <p>It is rumored that the new name is Meta.</p>
  <p>SFT</p>
  <p>I am sorry, I did not know that. I will try again.</p>
  <p>VRPO</p>
  <p>Yes, you are correct that the new name is Meta. Meta is the Greek wordfor “metamorphosis”, which refers to a change in form or appearance. Thecompany decided to change its name to reflect its focus on creating newways for people to connect and share experiences online. The new namealso has a positive connotation of transformation and innovation.</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Kai Ye</p>
</div>

---
layout: none
class: bg-white
title: "Thank you"
---

<img src="/slides/slide-26.svg" class="absolute inset-0 w-full h-full object-contain" alt="Slide 26: Thank you" />

<div class="sr-only">
  <h1>Thank you</h1>
  <p>THANK YOU</p>
  <p>Kai Ye</p>
  <p>k.ye1@lse.ac.uk</p>
  <p>https://github.com/VRPO/VRPO</p>
  <p>Our paper</p>
</div>
