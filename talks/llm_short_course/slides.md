---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Large Language Models (LLM) 
  A Guide to Principles and Training Method
drawings:
  persist: false
transition: slide-left
title: Large Language Models
mdc: true
routerMode: hash
fonts:
  sans: 'Inter, Noto Sans SC'
  serif: 'Merriweather'
  mono: 'Fira Code'
---

<style>
.slidev-layout h1 {
  border-bottom: 1px solid #010d21;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  font-weight: 700;
}

.slidev-layout {
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
}

.slidev-layout p, .slidev-layout li {
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  line-height: 1.6;
}

code {
  font-family: 'Fira Code', monospace;
}
</style>

# **Large Language Models (LLM)**

A Guide to Principles and Training Methods

<div class="pt-12 w-[680px] mx-auto">
  <div class="flex items-center justify-center gap-5">
    <span class="h-px w-24 bg-slate-400"></span>
    <strong class="text-2xl tracking-wide">Chengchun Shi</strong>
    <span class="h-px w-24 bg-slate-400"></span>
  </div>

  <div class="grid grid-cols-[1fr_auto_1fr] items-center mt-7">
    <div class="text-right pr-16">
      <strong class="text-xl tracking-wide">Kai Ye</strong>
    </div>
    <div class="w-px h-8 bg-slate-300"></div>
    <div class="text-left pl-10">
      <strong class="text-xl tracking-wide">Shijin Gong</strong>
    </div>
  </div>

  <div class="flex items-center justify-center gap-5 mt-5">
    <a href="https://noncollapse.github.io/" target="_blank" class="text-xl opacity-80 hover:opacity-100 transition-opacity" title="Homepage">
      🏠
    </a>
    <a href="https://scholar.google.com/citations?user=a7G8Yo8AAAAJ" target="_blank" class="text-xl opacity-80 hover:opacity-100 transition-opacity" title="Google Scholar">
      🎓
    </a>
    <a href="https://huggingface.co/Kyleyee" target="_blank" class="text-xl opacity-80 hover:opacity-100 transition-opacity" title="Hugging Face">
      🤗
    </a>
  </div>

  <div class="mt-3 text-sm tracking-[0.08em] opacity-70">
    LSE · Stats-Powered AI
  </div>
</div>

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Start <carbon:arrow-right class="inline"/>
  </span>
</div>

---
layout: default
---

# Table of Contents

<div class="mt-4 space-y-10 text-[0.88em] leading-tight">

<div>
  <h2 class="!text-3xl !mb-1"><a href="#/part-0-introduction" class="no-underline text-slate-900 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Part 0: Introduction to LLMs</a></h2>
</div>

<div>
  <h2 class="!text-3xl !mb-1"><a href="#/transformer-foundations" class="no-underline text-slate-900 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Part 1: LLM and Transformer Foundations</a></h2>
</div>

<div>
  <h2 class="!text-3xl !mb-1.5"><a href="#/part-2-training" class="no-underline text-slate-900 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Part 2: Three-Stage Training</a></h2>
  <ul class="!mt-0 !space-y-1">
    <li><a href="#/stage-1-pretraining" class="no-underline text-slate-700 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Stage 1: Pre-training</a></li>
    <li><a href="#/stage-2-sft" class="no-underline text-slate-700 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Stage 2: Supervised Fine-Tuning</a></li>
    <li><a href="#/stage-3-rlhf" class="no-underline text-slate-700 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Stage 3: Preference optimization and RLHF</a></li>
  </ul>
</div>

<div>
  <h2 class="!text-3xl !mb-1.5"><a href="#/part-3-reasoning" class="no-underline text-slate-900 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Part 3: The Development of Reasoning in LLMs</a></h2>
  <ul class="!mt-0 !space-y-1">
    <li><a href="#/inference-time-reasoning" class="no-underline text-slate-700 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Inference-Time Reasoning</a></li>
    <li><a href="#/rlvr" class="no-underline text-slate-700 hover:text-blue-600 hover:underline underline-offset-4 transition-colors">Reinforcement Learning with Verifiable Rewards</a></li>
  </ul>
</div>



</div>

---
layout: section
routeAlias: part-0-introduction
---

# Part 0: Introduction to LLMs

---
layout: full
title: Evolution of LLM
clicks: 5
routeAlias: intro-llms
---

<LLMEvolutionTimeline :step="$clicks" />

---
layout: full
title: What Is a GPT?
clicks: 3
---

<GPTIntroAnimation :step="$clicks"/>

---

# Number of LLMs Per Month (2024)

<div class="grid grid-cols-1 gap-6">

<img src="/figs/major_model_num.png" class="rounded"/>

<img src="/figs/derivate_model_num.png" class="rounded"/>

</div>

---

# This Year

<div class="mt-3 flex justify-center">
  <img
    src="/figs/kae-this-year.png"
    class="w-[94%] max-h-[520px] object-contain"
  />
</div>

---
layout: section
routeAlias: transformer-foundations
---

<h1 class="!text-[42px] !leading-tight whitespace-nowrap">Part 1: LLM and Transformer Foundations</h1>

<div class="text-2xl mt-8 opacity-80">
From <b>tokens and vectors</b> to <b>attention blocks</b>
</div>

---

# Before Transformer: How Do Words Become Numbers?

<div class="text-center text-2xl mt-8">
Understanding Embeddings is the <span class="text-blue-500 font-bold">KEY</span> to understanding Transformer
</div>

<div class="mt-18 grid grid-cols-3 gap-8">

<div class="text-center">
<div class="text-6xl mb-4">🐱</div>
<div class="text-xl">Cat</div>
<div class="text-sm opacity-70 mt-2">Human Language</div>
</div>

<div class="text-center flex items-center justify-center">
<div class="text-6xl -mt-16">→</div>
</div>

<div class="text-center">
<div class="text-4xl mb-4 font-mono">[0.2, 0.8, -0.1, ...]</div>
<div class="text-xl">Vector</div>
<div class="text-sm opacity-70 mt-2">Machine Understanding</div>
</div>

</div>

---

# Why Not Just Word IDs or One-Hot Encoding?

<div class="grid grid-cols-2 gap-8 mt-8">

<div>

## Simple Numbering ❌

```python
word_to_id = {
    "cat": 1,
    "airplane": 2,
    "kitten": 3,
    ...
    "dog": 9999
}
```

<div class="mt-6">

**Problems:**
- "cat" is closer to "airplane" than "dog"
- "dog" may be  more important than "airplane"
- A numeric index has no semantic meaning!

</div>

</div>

<div>

## One-Hot Encoding ❌

```python
vocab_size = 500000

"cat" → [1, 0, 0, 0, ..., 0]
"airplane" → [0, 1, 0, 0, ..., 0]
"kitten" → [0, 0, 1, 0, ..., 0]
...
"dog"→ [0, 0, 0, 0, ..., 1]
```

**Issues:**
-  Dimension = vocabulary size (huge!)
-  Sparse (99.9% are zeros)
-  No similarity (all perpendicular)


</div>

</div>

<div class="mt-4 p-4 bg-green-100 rounded text-center">
<strong>Key Idea:</strong> an efficient, trainable, and generalizable continuous space to support generalization.
</div>

---

# From One-Hot to Embedding

<div class="grid grid-cols-2 gap-8">

<div>

## What We Need ✓

<div class="mt-4">

**Semantic Distance:**
- Similar words → Close in a continuous space

</div>

<div class="mt-8 text-center">
<div class="text-base">
Cat 🐱 ≈ Dog 🐕 ≈ Kitten 🐈
</div>
<div class="text-sm opacity-60 mt-4">↕ (far)</div>
<div class="text-base mt-4">
Airplane ✈️
</div>
</div>

- high-dimensional one-hot vector → low-dimensional dense vector

$$ \operatorname{onehot}(i)^\top E = E[i] $$
</div>

<div>

## Embedding

```python
embedding_dim = 4096(Llama3) 
embedding_dim = 3584(Qwen2.5) 

"cat" → [0.2, 0.8, -0.1, ..., 0.5]
"dog" → [0.3, 0.7, -0.2, ..., 0.4]
"the" → [-0.5, 0.1, 0.9, ..., -0.2]
```

**Benefits:**
- ✓ Low dimension (e.g., 4096)
- ✓ Dense (all values meaningful)
- ✓ Cosine similarity captures meaning
- ✓ Learnable continuous starting representation



</div>

</div>


---

# Where Does Semantic Meaning Come From?

<div class="mt-4">

<div class="p-6 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl border-3 border-purple-300 mb-6">
<div class="text-2xl font-bold text-purple-800 mb-3">Critical 1: Task-Driven Learning</div>
<div class="text-lg">
 Embeddings are <span class="font-bold text-purple-700">learned automatically</span> during training to optimize task performance instead of Hand-Crafted.
</div>
</div>

<div class="grid grid-cols-2 gap-6">

<div>

<div class="px-5 pt-5 pb-2.5 bg-blue-50 rounded-lg border-2 border-blue-200">
<div class="text-lg font-bold text-blue-700 mb-2"> 💡 The Learning Process</div>
<div class="text-base leading-relaxed">

<div class="text-base leading-relaxed">
  If two tokens behave similarly in many contexts:
  <div class="mt-2 ml-4 text-sm opacity-90">
    • They appear in similar sentences and co-occur with similar words<br>
    • They help predict similar next tokens<br>
    • The loss produces similar gradients for their embeddings<br>
  </div>
  <div class="mt-2">
    → Gradient descent updates their vectors in similar directions, so they become
    <span class="text-blue-600 font-semibold">more similar</span>.
  </div>
</div>

</div>
</div>

</div>

<div>

<div class="p-5 bg-green-50 rounded-lg border-2 border-green-200 mb-4">
<div class="text-lg font-bold text-green-700 mb-3">🐱 Example: Semantic Similarity</div>
<div class="text-base mb-3">
      <code class="bg-white px-2 py-1 rounded">cat</code> and <code class="bg-white px-2 py-1 rounded">kitten</code> often appear in similar patterns:
    </div>
    <div class="text-sm italic opacity-80 ml-4">
      • "a ___ is a pet"<br>
      • "feed the ___"<br>
      • "the ___ is sleeping"
    </div>
    <div class="text-base mt-3">
      → Model updates their embeddings in similar directions
</div>
</div>


</div>

</div>

</div>


---

# Where Does Semantic Meaning Come From?

<div class="mt-4">

<div class="p-6 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl border-3 border-purple-300 mb-6">
<div class="text-2xl font-bold text-purple-800 mb-3">Critical 2: Embeddings are Dynamic</div>
<div class="text-lg">
In LLMs, the representation after Transformer layers creates <span class="font-bold text-purple-700">Contextual Embeddings</span> — the same token becomes different vectors in different contexts
</div>
</div>

<div class="grid grid-cols-2 gap-6">

<div>

<div class="px-5 pt-5 pb--2 bg-blue-50 rounded-lg border-2 border-blue-200">
<div class="text-lg font-bold text-blue-700 mb--4"> Pipeline</div>
<div class="text-base leading-relaxed">

1. **Start**: Static lookup + positional encoding

2. **Transform**: Apply self-attention + MLP layers repeatedly

3. **Result**: Each layer mixes information from other tokens. Final representation <span class="font-mono bg-white px-2 py-1 rounded">h_L</span> depends on full context.


</div>
</div>

</div>

<div>

<div class="p-5 bg-green-50 rounded-lg border-2 border-green-200 mb-4">
<div class="text-lg font-bold text-green-700 mb-3">🏦 Example: "bank"</div>
<div class="text-base mb-3">
<div class="bg-white p-3 rounded mb-2">
<span class="italic">"river <span class="font-bold text-blue-600">bank</span>"</span><br>
<span class="text-sm text-gray-600">→ Vector encodes "shoreline"</span>
</div>
<div class="bg-white p-3 rounded">
<span class="italic">"investment <span class="font-bold text-green-600">bank</span>"</span><br>
<span class="text-sm text-gray-600">→ Vector encodes "financial institution"</span>
</div>
</div>
</div>


</div>

</div>

</div>

---

# Tokenizer: From Text to Vocabulary IDs

<div class="text-[16px] mt-1">
We introduced the embedding lookup <b>E[i]</b>. <b>Where does the discrete index <i>i</i> come from?</b>
<div class="mt-1 text-[14px] leading-5 text-slate-600">
Subword tokenization shifts the basic unit from human-defined words to a learned vocabulary of reusable pieces.
</div>
</div>

<div class="grid grid-cols-[1.15fr_0.85fr] gap-8 mt-4">

<div>

## The tokenizer is the interface

<div class="mt-5 flex items-center justify-between text-center text-[13px]">
  <div class="w-[22%] py-3 border-y border-slate-300"><b>Raw text</b><br><span class="font-mono text-xs">"The cat sat."</span></div>
  <div class="text-slate-400 text-2xl">&rarr;</div>
  <div class="w-[22%] py-3 border-y border-amber-400"><b>Tokens</b><br><span class="font-mono text-xs">[The][ cat][ sat][.]</span></div>
  <div class="text-slate-400 text-2xl">&rarr;</div>
  <div class="w-[22%] py-3 border-y border-sky-400"><b>Token IDs</b><br><span class="font-mono text-xs">[31, 742, 581, 13]</span></div>
  <div class="text-slate-400 text-2xl">&rarr;</div>
  <div class="w-[18%] py-3 border-y border-emerald-400"><b>Vectors</b><br><span class="font-mono text-xs">E[31], ...</span></div>
</div>

<div class="mt-4 py-2 border-y border-slate-300 text-center font-mono text-[13px]">
token v<sub>i</sub> &harr; ID i &rarr; embedding row E[i]
</div>

<div class="mt-5 text-[15px] leading-6 space-y-2">
<div>The tokenizer owns a <b>fixed vocabulary</b> of allowed token strings.</div>
<div>Each vocabulary entry has one integer ID and one row in the embedding matrix.</div>
<div>The same tokenizer must be used during training and inference.</div>
</div>

</div>

<div class="border-l border-slate-300 pl-8">

## A toy vocabulary

<div class="mt-4 text-[13px]">
  <div class="grid grid-cols-[60px_1fr] py-2 border-b border-slate-300 font-bold text-slate-500"><span>ID</span><span>Token string</span></div>
  <div class="grid grid-cols-[60px_1fr] py-2 border-b border-slate-200"><span>13</span><span class="font-mono">"."</span></div>
  <div class="grid grid-cols-[60px_1fr] py-2 border-b border-slate-200"><span>31</span><span class="font-mono">"The"</span></div>
  <div class="grid grid-cols-[60px_1fr] py-2 border-b border-slate-200"><span>581</span><span class="font-mono">" sat"</span></div>
  <div class="grid grid-cols-[60px_1fr] py-2 border-b border-slate-200"><span>742</span><span class="font-mono">" cat"</span></div>
  <div class="grid grid-cols-[60px_1fr] py-2"><span>...</span><span>...</span></div>
</div>

<div class="mt-5 text-[13px] leading-5 text-slate-600">
The leading blank is often part of a token. Token boundaries therefore need not match word boundaries.
</div>

</div>

</div>

---

# Example: BPE Tokenization

<div class="text-[17px] mt-1">
Byte Pair Encoding (BPE) learns a compact subword vocabulary from frequent patterns in a training corpus.
</div>

<div class="grid grid-cols-[1.08fr_0.92fr] gap-9 mt-6">

<div>

## Building reusable pieces

<v-clicks>

<div class="mt-4">
  <div class="text-xs font-bold text-slate-500 mb-1">1. START FROM SMALL UNITS</div>
  <div class="font-mono text-[16px] tracking-[0.18em]">t o k e n i z a t i o n</div>
</div>

<div class="mt-5">
  <div class="text-xs font-bold text-slate-500 mb-1">2. MERGE FREQUENT ADJACENT PAIRS</div>
  <div class="font-mono text-[15px]">t + o &rarr; to&nbsp;&nbsp;&nbsp; e + n &rarr; en&nbsp;&nbsp;&nbsp; i + zation &rarr; ization</div>
</div>

<div class="mt-5">
  <div class="text-xs font-bold text-slate-500 mb-2">3. APPLY THE LEARNED MERGE RULES</div>
  <div class="flex items-center gap-3">
    <span class="px-4 py-2 bg-amber-100 border border-amber-400 rounded font-mono font-bold">token</span>
    <span class="text-slate-400">+</span>
    <span class="px-4 py-2 bg-sky-100 border border-sky-400 rounded font-mono font-bold">ization</span>
  </div>
</div>

</v-clicks>

<div class="mt-7 pt-4 border-t border-slate-300 text-[14px] leading-6">
Frequent strings become single vocabulary entries; rare or unseen strings can still be represented by smaller pieces.
</div>

</div>

<div class="border-l border-slate-300 pl-8">

## Not words, but tokens!

<div class="mt-4 text-[14px] leading-6">
A token may be a whole word, a subword, punctuation, whitespace, or a byte-level piece.
</div>

<div class="mt-2 text-[11px] text-slate-500">Illustrative output; exact pieces and IDs depend on the learned vocabulary.</div>

<div class="mt-4 font-mono text-[13px] leading-8">
  <div><span class="text-slate-500">text&nbsp;&nbsp;&nbsp;</span> "tokenization is important"</div>
  <div><span class="text-slate-500">tokens&nbsp;</span> ["token", "ization", " is", " import", "ant"]</div>
  <div><span class="text-slate-500">IDs&nbsp;&nbsp;&nbsp;&nbsp;</span> [5963, 2065, 374, 2928, 519]</div>
</div>

<div class="mt-4 space-y-2 text-[13px]">
  <div><b>Common text:</b> fewer, larger tokens</div>
  <div><b>Rare or unseen text:</b> more, smaller units instead of an unknown word</div>
</div>

</div>

</div>

---


# Positional Encoding: Teaching Position to Transformers

<div class="text-center text-xl mt-6">
🤔 Problem: Embeddings have <span class="text-red-500">no position information</span>!
</div>

<div class="grid grid-cols-2 gap-8 mt-8">

<div>

**Same embeddings, different meanings:**

```
"The cat chased the dog"
"The dog chased the cat"
```

<div class="mt-4">
Without position info, these look <span class="text-red-500">identical</span> to the model!
</div>

<div class="mt-4 p-4 bg-blue-50 border-2 border-blue-300 rounded-lg">
<div class="text-center text-lg">

$$ \mathrm{Attn}(PX) = P\,\mathrm{Attn}(X) $$
</div>
</div>

</div>

<div>

**Solution: Add Position Information**

<v-clicks>

1. Construct a position vector for each sequence index

2. Add it to the corresponding token embedding

3. The same token now has a different representation at each position

</v-clicks>

</div>

</div>

---

# Example: Sinusoidal Positional Encoding

<div class="grid grid-cols-2 gap-6">

<div>

## Core Idea

Use sine and cosine functions to encode position:

$$
\begin{aligned}
PE(pos, 2i) &= \sin\left(\frac{pos}{10000^{2i/d}}\right) \\
PE(pos, 2i+1) &= \cos\left(\frac{pos}{10000^{2i/d}}\right)
\end{aligned}
$$

<div class="mt-4">

- `pos`: position in sequence (0, 1, 2, ...)
- `i`: dimension index
- `d`: embedding dimension (e.g., 4096)

<div class="mt-2">

- **High-frequency** dimensions change **rapidly**, helping the model distinguish nearby positions 

- **Low-frequency** dimensions vary **slowly**, providing long-range positional signals 
</div>
</div>

</div>

<div>

## How to Use

<div class="mt-4">

**Simple: Just add them element-wise!**

$$
\boxed{\text{Final Vector} = \text{Embedding} + \text{Position Encoding}}
$$

</div>

<div class="mt--2">

<style>
  .vector-box {
    display: inline-flex;
    width: 45px;
    height: 45px;
    border: 2px solid #333;
    border-radius: 6px;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 13px;
    margin: 2px;
    transition: all 0.5s ease;
  }
  .embed-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  .pos-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
  }
  .result-box {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }
  .vector-row {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 12px 0;
  }
  .operator {
    font-size: 28px;
    font-weight: bold;
    margin: 0 10px;
    color: #333;
  }
  .label {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 8px;
    text-align: center;
  }
  .merge-box {
    background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
    color: white;
  }
  .overlay-wrap {
    display: grid;
  }
  .overlay-item {
    grid-area: 1 / 1;
  }
  .merge-block {
    opacity: 1;
    animation: merge-fade 1.0s ease forwards;
  }
  .result-fade {
    opacity: 0;
    animation: result-fade 0.6s ease forwards;
    animation-delay: 0.6s;
  }
  @keyframes merge-fade {
    0% { opacity: 1; transform: scale(1); }
    60% { opacity: 1; transform: scale(0.99); }
    100% { opacity: 0; transform: scale(0.99); }
  }
  @keyframes result-fade {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
</style>

<div class="text-center text-lg font-bold mb-0">
Token "cat" at Position 1
</div>

<div v-show="$slidev.nav.clicks < 3">
  <!-- Step 1: Show Embedding (visible on click 1 and 2, hidden on click 3+) -->
  <div v-click="1" class="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
    <div class="label" style="color: #667eea;">🟣 Token Embedding</div>
    <div class="vector-row">
      <div class="vector-box embed-box">0.3</div>
      <div class="vector-box embed-box">-0.4</div>
      <div class="vector-box embed-box">0.6</div>
      <div class="vector-box embed-box">0.2</div>
      <div class="vector-box embed-box">-0.1</div>
      <div class="vector-box embed-box">0.8</div>
    </div>
  </div>

  <!-- Step 2: Show Position Encoding (visible on click 2, hidden on click 3+) -->
  <div v-click="2" class="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg mt-2">
    <div class="label" style="color: #f093fb;">🔴 Position Encoding (pos=1)</div>
    <div class="vector-row">
      <div class="vector-box pos-box">0.8</div>
      <div class="vector-box pos-box">0.5</div>
      <div class="vector-box pos-box">0.1</div>
      <div class="vector-box pos-box">0.9</div>
      <div class="vector-box pos-box">0.2</div>
      <div class="vector-box pos-box">-0.3</div>
    </div>
  </div>
</div>

<span v-click="3" class="hidden"></span>

<!-- Step 3: Overlay container for merge animation -->
<div class="relative mt-4" style="min-height: 150px;">
  <!-- Step 3a: Show Merged Vector (on click 3, then fade out) -->
  <div v-show="$slidev.nav.clicks >= 3" class="absolute top-0 left-0 right-0 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg merge-block">
    <div class="label" style="color: #7b5bd6;">🟣 Embedding + Position Encoding</div>
    <div class="vector-row">
      <div class="vector-box merge-box">1.1</div>
      <div class="vector-box merge-box">0.1</div>
      <div class="vector-box merge-box">0.7</div>
      <div class="vector-box merge-box">1.1</div>
      <div class="vector-box merge-box">0.1</div>
      <div class="vector-box merge-box">0.5</div>
    </div>
  </div>

  <!-- Step 3b: Show Final Result (fade in after merge) -->
  <div v-show="$slidev.nav.clicks >= 3" class="absolute top-0 left-0 right-0 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg result-fade">
    <div class="label" style="color: #4facfe;">🔵 Final Result (Position-aware)</div>
    <div class="vector-row">
      <div class="vector-box result-box">1.1</div>
      <div class="vector-box result-box">0.1</div>
      <div class="vector-box result-box">0.7</div>
      <div class="vector-box result-box">1.1</div>
      <div class="vector-box result-box">0.1</div>
      <div class="vector-box result-box">0.5</div>
    </div>
    <div class="mt-3 text-center text-xs text-gray-600">
      ✨ Now each token has unique position information embedded!
    </div>
  </div>
</div>

</div>

</div>

</div>

---
layout: section
---

# Transformer Architecture

---

# From Vectors to Transformer Blocks

<div class="grid grid-cols-[0.92fr_1.08fr] gap-8 mt-0 items-center">

<div class="text-[15px] leading-6">

After tokenization and positional encoding, every token is represented by a vector:

$$
h_i^{(0)} = e_i + p_i, \qquad
H^{(0)} = [h_1^{(0)},\ldots,h_T^{(0)}]^{\top}\in\mathbb{R}^{T\times d}.
$$

The sequence is now a matrix of numbers, so it can be processed by the neural-network layers inside a Transformer.

<div class="mt-4 space-y-2.5">

<div><b class="text-amber-700">Attention</b> mixes information across token positions.</div>

<div><b class="text-sky-700">Feed-forward layers</b> transform each token representation.</div>

<div><b class="text-lime-700">Residual connections and normalization</b> make many blocks trainable as a deep network.</div>

</div>

<div class="mt-4 pt-3 border-t border-slate-300 text-[13px] leading-5 text-slate-600">
The original Transformer uses an <b>encoder</b> and a <b>decoder</b>. Next, we unpack the repeated block shared by this architecture.
</div>

</div>

<div class="flex flex-col items-center">
  <img
    src="/figs/transformer-original-architecture.png"
    class="h-[430px] w-full object-contain"
    alt="Original Transformer encoder-decoder architecture"
  />
  <div class="mt-1 text-[10px] text-slate-500">
    Vaswani et al. (2017), <i>Attention Is All You Need</i>, Figure 1.
  </div>
</div>

</div>

---

# Attention: Why Context Matters

<div class="text-base leading-relaxed">

Consider the sentence: "*The animal crossed the street because it was tired.*"

<div class="mt-4 p-4 bg-blue-50 rounded">

In this sentence, **it** is a pronoun. What does it refer to?

- Does it refer to **animal** or **street**?
- This question is simple for humans, but not so easy for models

</div>
<div class="mt-6 grid grid-cols-2 gap-6">

<div>

**RNN's Approach**

- When processing a word, considers the hidden state from previous words
- Hidden state contains information from preceding words
- Sequential processing, chain-like information flow

</div>

<div>

**Self Attention's Advantage**

- Current token **directly attends** to all available earlier tokens
- Parallel processing, direct long-range dependencies
- As illustrated in the "it" example below

</div>

</div>

</div>

---

# Attention: Weighted Information Aggregation

<div class="text-[17px] leading-7 mt-1">
At position <i>t</i>, attention constructs a new representation by deciding <b>how much information to take from each available token</b>.
</div>

<div class="grid grid-cols-[1.23fr_0.77fr] gap-10 mt-5">

<div class="min-w-0">

<div class="flex items-center gap-1.5 font-mono text-[13px] mb-3">
  <span class="px-2 py-1 bg-slate-100 rounded">The</span>
  <span class="px-2 py-1 bg-slate-100 rounded">animal</span>
  <span class="px-2 py-1 bg-slate-100 rounded">crossed</span>
  <span class="px-2 py-1 bg-slate-100 rounded">the</span>
  <span class="px-2 py-1 bg-slate-100 rounded">street</span>
  <span class="px-2 py-1 bg-slate-100 rounded">because</span>
  <span class="px-2 py-1 bg-amber-100 border border-amber-400 rounded font-bold">it</span>
  <span class="px-2 py-1 border border-dashed border-slate-300 rounded text-slate-400">was</span>
  <span class="px-2 py-1 border border-dashed border-slate-300 rounded text-slate-400">tired</span>
</div>

<div class="space-y-1.5 text-[12px]">
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>The</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-300" style="width: 5%"></div></div><span>0.05</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>animal</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-500" style="width: 45%"></div></div><span>0.45</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>crossed</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-300" style="width: 10%"></div></div><span>0.10</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>the</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-300" style="width: 5%"></div></div><span>0.05</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>street</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-400" style="width: 20%"></div></div><span>0.20</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>because</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-300" style="width: 5%"></div></div><span>0.05</span></div>
  <div class="grid grid-cols-[62px_1fr_42px] gap-3 items-center"><b>it</b><div class="h-4 bg-slate-100 rounded-full overflow-hidden"><div class="h-full bg-amber-400" style="width: 10%"></div></div><span>0.10</span></div>
</div>

<div class="mt-5 text-center text-[0.95em]">
$$
z_t = \sum_{j=1}^{t}\alpha_{tj}v_j,
\qquad \alpha_{tj}\ge 0,
\qquad \sum_{j=1}^{t}\alpha_{tj}=1.
$$
</div>

<div class="mt-1 text-[14px] text-slate-600">
The weights <i>&alpha;</i><sub>tj</sub> depend on the current position and determine which historical value vectors <i>v</i><sub>j</sub> contribute most.
</div>

</div>

<div class="min-w-0 border-l border-slate-300 pl-8">

<div class="text-lg font-bold mb-1">Repeated context mixing</div>
<div class="text-[11px] text-slate-500 mb-2">every position &times; every head &times; every Transformer block</div>

<div class="text-center text-[13px] leading-4">
  <div class="font-semibold">Input vectors <i>H</i><sup>(0)</sup></div>
  <div class="my-0.5 text-slate-400 text-base">&darr;</div>
  <div class="py-1 border-y border-amber-300"><b>Block 1 attention</b></div>
  <div class="my-0.5 text-slate-400 text-base">&darr;</div>
  <div class="font-semibold">Contextual vectors <i>H</i><sup>(1)</sup></div>
  <div class="my-0.5 text-slate-400 text-base">&darr;</div>
  <div class="py-1 border-y border-sky-300"><b>Block 2 attention</b></div>
  <div class="my-0.5 text-slate-400 text-base">&darr;</div>
  <div class="text-slate-400">...</div>
  <div class="my-0.5 text-slate-400 text-base">&darr;</div>
  <div class="font-semibold">Final vectors <i>H</i><sup>(L)</sup></div>
</div>

</div>

</div>
---

# Queries, Keys, and Values: Match, Then Retrieve

<div class="text-[17px] leading-7 mt-1">
At the current position <i>t</i>, self-attention first decides <b>where to read</b>, then retrieves the information stored there.
</div>

<div class="grid grid-cols-[0.95fr_1.05fr] gap-10 mt-7 items-center">

<div class="space-y-5 text-[14px] leading-6">
  <div class="border-l-4 border-amber-400 pl-4">
    <div class="text-lg font-bold text-amber-700">Query</div>
    <div class="font-serif italic text-lg">q<sub>t</sub> = h<sub>t</sub>W<sub>Q</sub></div>
    <div>What information does the current token need?</div>
  </div>

  <div class="border-l-4 border-sky-400 pl-4">
    <div class="text-lg font-bold text-sky-700">Key</div>
    <div class="font-serif italic text-lg">k<sub>j</sub> = h<sub>j</sub>W<sub>K</sub></div>
    <div>What could source token <i>j</i> provide?</div>
  </div>

  <div class="border-l-4 border-emerald-400 pl-4">
    <div class="text-lg font-bold text-emerald-700">Value</div>
    <div class="font-serif italic text-lg">v<sub>j</sub> = h<sub>j</sub>W<sub>V</sub></div>
    <div>What content is passed forward if token <i>j</i> is selected?</div>
  </div>
</div>

<div class="text-center">
  <div class="font-mono text-[13px] whitespace-nowrap mb-5">
    The animal crossed the street because <span class="px-2 py-1 bg-amber-100 border border-amber-400 rounded font-bold">it</span> was tired
  </div>

  <div class="text-[14px] leading-6 space-y-2">
    <div><b>1. Match</b> the query with every available key</div>
    <div class="font-serif italic text-lg">s<sub>tj</sub> = q<sub>t</sub><sup>T</sup>k<sub>j</sub> / &radic;d<sub>k</sub></div>
    <div class="text-xl text-slate-400">&darr;</div>
    <div><b>2. Normalize</b> the scores into attention weights</div>
    <div class="font-serif italic text-lg">&alpha;<sub>tj</sub> = softmax<sub>j</sub>(s<sub>tj</sub>)</div>
    <div class="text-xl text-slate-400">&darr;</div>
    <div><b>3. Retrieve</b> a weighted combination of values</div>
    <div class="font-serif italic text-lg">z<sub>t</sub> = &Sigma;<sub>j</sub> &alpha;<sub>tj</sub>v<sub>j</sub></div>
  </div>

</div>

</div>

---

# Self-Attention Computation

<div class="text-center mb-4 text-2xl">
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V
$$
</div>

<div class="text-center text-xs text-slate-500 mt--3">
<i>M</i> is the causal mask: future positions receive zero attention weight.
</div>

<div class="flex items-center justify-center mt-10">

<div class="flex items-center gap-4">

<!-- Score Matrix -->
<div class="flex flex-col items-center">
<div class="text-gray-600 font-bold text-sm mb-2">Q×K<sup>T</sup> (n×n)</div>
<div class="grid grid-cols-4 gap-1">
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
<div class="w-8 h-8 bg-gray-200 border-2 border-gray-400"></div>
</div>
</div>

<!-- Arrow and softmax -->
<div class="flex flex-col items-center gap-1">
<div class="text-2xl">→</div>
<div class="text-sm">softmax</div>
</div>

<!-- Attention Weights -->
<div class="flex flex-col items-center">
<div class="text-green-600 font-bold text-sm mb-2">Attention weights A (n×n)</div>
<div class="grid grid-cols-4 gap-1">
<div class="w-8 h-8 bg-green-100 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-green-500 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-300 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-green-200 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-400 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-500 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-slate-100 border-2 border-slate-300"></div>
<div class="w-8 h-8 bg-green-100 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-300 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-400 border-2 border-green-400"></div>
<div class="w-8 h-8 bg-green-200 border-2 border-green-400"></div>
</div>
</div>

<div class="text-2xl">×</div>

<!-- V Matrix -->
<div class="flex flex-col items-center">
<div class="text-blue-500 font-bold text-sm mb-2">V (n×d)</div>
<div class="grid grid-cols-3 gap-1">
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
<div class="w-8 h-8 bg-blue-200 border-2 border-blue-400"></div>
</div>
</div>

<div class="text-2xl">=</div>

<!-- Z Matrix -->
<div class="flex flex-col items-center">
<div class="text-pink-500 font-bold text-sm mb-2">Z (n×d)</div>
<div class="grid grid-cols-3 gap-1">
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
<div class="w-8 h-8 bg-pink-200 border-2 border-pink-400"></div>
</div>
</div>

</div>

</div>

---

# Self-Attention: From Formula to Code

<div class="grid grid-cols-[1.08fr_0.92fr] gap-8 mt-3">

<div>

```python
def causal_self_attention(H, W_Q, W_K, W_V):
    Q = H @ W_Q
    K = H @ W_K
    V = H @ W_V

    scores = Q @ K.transpose(-2, -1)
    scores = scores / sqrt(K.size(-1))
    scores = scores.masked_fill(future_mask, -inf)

    A = softmax(scores, dim=-1)
    Z = A @ V
    return Z
```

</div>

<div class="text-[15px] leading-6">

<div class="text-[22px] font-bold mb-2">The same computation in four lines</div>

$$
Q=HW_Q,\qquad K=HW_K,\qquad V=HW_V
$$

$$
S=\frac{QK^{\top}}{\sqrt{d_k}},
\qquad
A=\operatorname{softmax}(S+M)
$$

$$
Z=AV
$$

<div class="mt-5 border-t border-slate-300 pt-4 space-y-2 text-[13px] text-slate-600">
<div><b><i>S</i><sub>tj</sub></b>: compatibility between current position <i>t</i> and source position <i>j</i>.</div>
<div><b><i>A</i><sub>tj</sub></b>: normalized attention weight after the causal mask.</div>
<div><b><i>Z</i><sub>t</sub></b>: weighted aggregation of the available value vectors.</div>
</div>

</div>

</div>

---

# Multi-Head Attention



<div>

- **Concatenate all the attention heads**

- **Multiply with a weight matric $W^0$**

- **The output $Z$ captures information from all the attention heads**



</div>

<div class="flex items-center justify-center mt--8 pt-4 gap-6">

<!-- Concatenated Z1-Z8: each Z is 4×3, concat to 4×24 -->
<div class="flex flex-col items-center gap-2">
<div class="flex gap-2 text-xs font-semibold mb-1">
<span class="w-12 text-center">Z1</span>
<span class="w-12 text-center">Z2</span>
<span class="w-12 text-center">Z3</span>
<span class="w-12 text-center">Z4</span>
<span class="w-12 text-center">Z5</span>
<span class="w-12 text-center">Z6</span>
<span class="w-12 text-center">Z7</span>
<span class="w-12 text-center">Z8</span>
</div>
<div class="grid grid-cols-24 gap-0.5">
<!-- 4 rows × 24 cols = 96 squares total -->
<div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div>
<div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div>
<div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div>
<div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-200 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div><div class="w-4 h-4 bg-pink-300 border border-pink-300"></div>
</div>
<div class="text-sm font-semibold">Concat (n×(d<sub>v</sub>·m))</div>
</div>

<!-- Multiply symbol -->
<div class="text-3xl">×</div>

<!-- Linear transformation matrix: 24×5 -->
<div class="flex flex-col items-center gap-2">
<div class="grid grid-cols-5 gap-0.5 max-h-64">
<!-- 24 rows × 5 cols = 120 squares (竖长矩阵) -->
<div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div><div class="w-2 h-2 bg-pink-100 border border-pink-300"></div>
</div>
<div class="text-sm font-semibold text-center">Weight matrix (d<sub>v</sub>·m×d)</div>
</div>

<!-- Equal symbol -->
<div class="text-3xl">=</div>

<!-- Final output Z: 4×5 -->
<div class="flex flex-col items-center gap-2">
<div class="text-sm font-semibold mb-1">Output Z</div>
<div class="grid grid-cols-5 gap-0.5">
<div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div>
<div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div>
<div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div>
<div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div><div class="w-7 h-7 bg-pink-300 border-2 border-pink-400"></div>
</div>
<div class="text-xs">(nxd) which is same as the input X</div>
</div>

</div>

---

# Multi-Head Attention: Visualizing Different Heads

<div class="mt-4">

**After learning multi-head attention, let's revisit the "it" example we mentioned earlier and see what different attention heads focus on.**

**The green and orange colors represent two different attention heads:**

</div>

<div class="flex flex-col items-center justify-center mt-8 gap-8">

<!-- Top row: Input tokens (horizontal) -->
<div class="flex flex-col gap-3">
<div class="text-sm font-semibold text-center mb-2">Input Tokens</div>
<div class="flex gap-2">
<div class="px-3 py-2 bg-orange-300 border-2 border-orange-400 rounded text-xs">The_</div>
<div class="px-3 py-2 bg-orange-300 border-2 border-orange-400 rounded text-xs font-semibold">animal_</div>
<div class="px-3 py-2 bg-orange-100 border border-orange-300 rounded text-xs">didn_</div>
<div class="px-3 py-2 bg-orange-100 border border-orange-200 rounded text-xs">'_</div>
<div class="px-3 py-2 bg-orange-200 border border-orange-200 rounded text-xs">t_</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs">cross_</div>
<div class="px-3 py-2 bg-orange-50 border border-orange-200 rounded text-xs">the_</div>
<div class="px-3 py-2 bg-orange-50 border border-orange-200 rounded text-xs">street_</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs">because_</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs">it_</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs">was_</div>
<div class="px-3 py-2 bg-orange-50 border border-orange-200 rounded text-xs">too_</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs font-semibold">tire</div>
<div class="px-3 py-2 bg-orange-20 border border-orange-200 rounded text-xs font-semibold">d_</div>
</div>
</div>
<div class="flex flex-col gap-3">
<div class="flex gap-2">
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">The_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">animal_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">didn_</div>
<div class="px-3 py-2 bg-green-20 border border-green-200 rounded text-xs">'_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">t_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">cross_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">the_</div>
<div class="px-3 py-2 bg-green-50 border border-green-300 rounded text-xs">street_</div>
<div class="px-3 py-2 bg-green-20 border border-green-300 rounded text-xs">because_</div>
<div class="px-3 py-2 bg-purple-20 border border-green-300 rounded text-xs font-semibold">it_</div>
<div class="px-3 py-2 bg-green-100 border border-green-300 rounded text-xs">was_</div>
<div class="px-3 py-2 bg-green-100 border border-green-300 rounded text-xs">too_</div>
<div class="px-3 py-2 bg-green-300 border-2 border-green-500 rounded text-xs">tire</div>
<div class="px-3 py-2 bg-green-300 border-2 border-green-500 rounded text-xs">d_</div>
</div>
</div>
<!-- Bottom row: Output tokens (horizontal) with "it" highlighted -->
<div class="flex flex-col gap-3">
<div class="flex gap-2">
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">The_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">animal_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">didn_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">'_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">t_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">cross_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">the_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">street_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">because_</div>
<div class="px-3 py-2 bg-purple-200 border-2 border-purple-500 rounded text-xs font-semibold">it_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">was_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">too_</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">tire</div>
<div class="px-3 py-2 bg-gray-100 border border-gray-300 rounded text-xs">d_</div>
</div>
</div>

</div>

<div class="mt-6 text-sm">
<div class="flex gap-8 justify-center">
<div class="flex items-center gap-2">
<div class="w-4 h-4 bg-orange-300 border-2 border-orange-500"></div>
<span><b>Orange Head:</b> "it" attends to "The animal"</span>
</div>
<div class="flex items-center gap-2">
<div class="w-4 h-4 bg-green-400 border-2 border-green-600"></div>
<span><b>Green Head:</b> "it" attends to "tired"</span>
</div>
</div>
</div>

---

# Feed-Forward Networks and Add & Norm

<div class="mt-6">

**After Multi-Head Attention, each token representation passes through:**

</div>

<div class="grid grid-cols-2 gap-8 mt-8">

<!-- Feed-Forward Network -->
<div class="flex flex-col gap-4">
<div class="text-lg font-bold text-blue-600">1. Feed-Forward Network (FFN)</div>

<div class="bg-blue-50 p-4 rounded">

**Two-layer neural network applied to each position independently:**

$$
\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2
$$

- **First layer**: Expands dimension (e.g., 512 → 2048)
- **Second layer**: Projects back (e.g., 2048 → 512)

</div>

<div class="text-sm mt-2">
💡 Purpose: Add non-linearity and learn complex patterns
</div>

</div>

<!-- Add & Norm -->
<div class="flex flex-col gap-4">
<div class="text-lg font-bold text-green-600">2. Add & Norm (Residual + Layer Norm)</div>

<div class="bg-green-50 p-4 rounded">

**Residual Connection + Layer Normalization:**

$$
\text{LayerNorm}(x + \text{Sublayer}(x))
$$

<div class="mt-3">

**Two applications in each transformer block:**
- Around Multi-Head Attention
- Around Feed-Forward Network

</div>

<div class="mt-3 text-sm">



</div>

</div>

<div class="text-sm mt-2">
💡 Purpose: Helps gradient flow in deep networks and Stabilizes training
</div>

</div>

</div>

---

# Encoder and Decoder

<div class="mt-4 text-sm">

**The original Transformer has two main components. Most generative LLMs later keep only the causal decoder stack:**

</div>

<div class="grid grid-cols-2 gap-8 mt-6">

<!-- Encoder -->
<div class="flex flex-col gap-4">
<div class="text-xl font-bold text-blue-600">📥 Encoder</div>

<div class="bg-blue-50 p-4 rounded">

**Purpose**: Understanding input sequence

**Key Features**:
- **Bidirectional** attention (can see all tokens)
- Good for: Understanding, classification

</div>


</div>

<!-- Decoder -->
<div class="flex flex-col gap-4">
<div class="text-xl font-bold text-green-600">📤 Decoder</div>

<div class="bg-green-50 p-4 rounded">

**Purpose**: Generate output sequence 

**Key Features**:
- **Unidirectional** (masked) attention
- Good for: Generation, translation

</div>

</div>

</div>

<div class="mt-2 p-4 bg-gray-100 rounded">

**Both contain many Transformer Blocks:**

Input → **Multi-Head Attention** → Add & Norm → **Feed-Forward** → Add & Norm → Output

</div>

---

# Encoder: Every Token Reads the Full Input

<div class="text-[17px] leading-7 mt-1">
An encoder receives the complete input sequence at once. Each position can attend to <b>every other input position</b>.
</div>

<div class="grid grid-cols-[0.92fr_1.08fr] gap-12 mt-7 items-center">

<div>
  <div class="font-mono text-[15px] flex justify-center gap-3 mb-5">
    <span class="px-3 py-2 bg-sky-50 border border-sky-300 rounded">The</span>
    <span class="px-3 py-2 bg-sky-50 border border-sky-300 rounded">river</span>
    <span class="px-3 py-2 bg-sky-100 border border-sky-400 rounded font-bold">bank</span>
    <span class="px-3 py-2 bg-sky-50 border border-sky-300 rounded">flooded</span>
  </div>

  <div class="text-center text-xs font-bold text-slate-500 mb-2">KEY POSITIONS</div>
  <div class="grid grid-cols-[58px_repeat(4,48px)] gap-1 items-center justify-center text-center text-[11px]">
    <div></div><div>The</div><div>river</div><div>bank</div><div>flooded</div>
    <div class="text-right pr-2">The</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div>
    <div class="text-right pr-2">river</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-200">visible</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div>
    <div class="text-right pr-2 font-bold text-sky-700">bank</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-300">visible</div><div class="py-2.5 bg-sky-200">visible</div><div class="py-2.5 bg-sky-100">visible</div>
    <div class="text-right pr-2">flooded</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-100">visible</div><div class="py-2.5 bg-sky-200">visible</div>
  </div>
  <div class="text-center text-[11px] text-slate-500 mt-2">QUERY POSITIONS</div>
</div>

<div class="text-[15px] leading-7">

<div class="text-center text-[0.95em] mb-4">

$$
H_{\mathrm{enc}}=\operatorname{Encoder}(H^{(0)})
=\left[h_1,\ldots,h_T\right]^{\top}.
$$

</div>

<div class="space-y-4">
  <div><b>One contextual vector per input token.</b> The output length is still T.</div>
  <div><b>Context changes meaning.</b> The representation of “bank” incorporates “river” and “flooded”.</div>
  <div><b>No autoregressive generation is required.</b> All input positions are processed together.</div>
</div>

<div class="mt-5 pt-3 border-t border-slate-300 text-[12px] whitespace-nowrap text-slate-600">
Examples: classification, retrieval, token labeling, and encoder-decoder source states.
</div>

</div>

</div>

---

# Decoder-Only Transformer: The GPT Architecture

<div class="text-[17px] leading-7 mt-1">
The GPT series uses a <b>decoder-only Transformer</b>: causal self-attention converts next-token prediction into both its training objective and its generation mechanism.
</div>

<div class="mt-7 flex items-center justify-center gap-4 text-center text-[13px]">
  <div class="font-mono flex items-center gap-1.5">
    <span class="px-2 py-2 bg-slate-100 border border-slate-300 rounded">The</span>
    <span class="px-2 py-2 bg-slate-100 border border-slate-300 rounded">answer</span>
    <span class="px-2 py-2 bg-slate-100 border border-slate-300 rounded">is</span>
  </div>
  <div class="text-2xl text-slate-400">&rarr;</div>
  <div class="w-[185px] py-4 border-y-2 border-amber-500 font-bold">Causal decoder blocks</div>
  <div class="text-2xl text-slate-400">&rarr;</div>
  <div class="w-[115px] py-4 border-y border-sky-400">final state<br><span class="font-serif italic">h<sub>t</sub><sup>(L)</sup></span></div>
  <div class="text-2xl text-slate-400">&rarr;</div>
  <div class="w-[150px] py-4 border-y border-emerald-400">LM head<br><span class="font-mono text-[11px]">W<sub>lm</sub> + softmax</span></div>
  <div class="text-2xl text-slate-400">&rarr;</div>
  <div class="w-[145px] py-4 border-y-2 border-fuchsia-400 font-bold">next-token<br>distribution</div>
</div>

<div class="grid grid-cols-[0.9fr_1.1fr] gap-12 mt-8 items-center">

<div class="text-center border-r border-slate-300 pr-8 text-[0.9em]">
  <div class="text-[15px] font-bold mb-1">One forward pass</div>

  <div class="mt-4 font-serif italic text-[17px] leading-8">
    <div>p<sub>&theta;</sub>(y<sub>t+1</sub> | x, y<sub>1:t</sub>)</div>
    <div>= softmax(W<sub>lm</sub>h<sub>t</sub><sup>(L)</sup> + b)</div>
  </div>

  <div class="mt-4 font-serif italic text-[17px] leading-8">
    p<sub>&theta;</sub>(y<sub>1:T</sub> | x)
    = &prod;<sub>t=1</sub><sup>T</sup> p<sub>&theta;</sub>(y<sub>t</sub> | x, y<sub>&lt;t</sub>)
  </div>

  <div class="mt-5 pt-3 border-t border-slate-300 text-left text-[12px] leading-5 text-slate-600">
    <div><b>Original decoder:</b> causal self-attention + encoder cross-attention.</div>
    <div><b>GPT decoder:</b> causal self-attention only.</div>
  </div>

</div>

<div>
  <div class="text-[15px] font-bold mb-4">Autoregressive generation</div>
  <div class="font-mono text-[13px] space-y-3">
    <div class="flex items-center gap-2">
      <span class="px-2 py-1 bg-slate-100 rounded">The answer is</span>
      <span>&rarr;</span>
      <span class="px-2 py-1 bg-emerald-100 border border-emerald-400 rounded font-bold">42</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="px-2 py-1 bg-slate-100 rounded">The answer is 42</span>
      <span>&rarr;</span>
      <span class="px-2 py-1 bg-emerald-100 border border-emerald-400 rounded font-bold">.</span>
    </div>
  </div>

  <div class="mt-5 text-[14px] leading-6">
    <div><b>Training:</b> the causal mask allows next-token losses at all positions to be computed in parallel.</div>
    <div class="mt-2"><b>Inference:</b> sample one token, append it to the prefix, and run the decoder again until EOS.</div>
  </div>
</div>

</div>

---

# From the Original Transformer to BERT and GPT

<div class="grid grid-cols-[1fr_460px_1fr] gap-7 mt-2 items-center h-[445px]">

<div class="text-center">
  <div class="text-[14px] font-bold tracking-[0.14em] uppercase text-sky-700">Encoder only</div>
  <div class="mt-3 text-4xl font-bold">BERT</div>
  <div class="mt-3 text-[13px] leading-5 text-slate-600">
    Bidirectional self-attention builds contextual representations of the input.
  </div>
  <div class="mt-7 flex items-center justify-end gap-3 text-sky-600">
    <span class="text-[12px] font-semibold">keep the encoder</span>
    <span class="text-4xl leading-none">&larr;</span>
  </div>
</div>

<div class="flex flex-col items-center">
  <img
    src="/figs/transformer-original-architecture.png"
    class="h-[410px] w-full object-contain"
    alt="Original Transformer encoder-decoder architecture"
  />
  <div class="mt-[-4px] text-[10px] text-slate-500">
    Vaswani et al. (2017), <i>Attention Is All You Need</i>, Figure 1.
  </div>
</div>

<div class="text-center">
  <div class="text-[14px] font-bold tracking-[0.14em] uppercase text-amber-700">Decoder only</div>
  <div class="mt-3 text-4xl font-bold">GPT</div>
  <div class="mt-3 text-[13px] leading-5 text-slate-600">
    Causal self-attention predicts and generates the next token autoregressively.
  </div>
  <div class="mt-7 flex items-center justify-start gap-3 text-amber-600">
    <span class="text-4xl leading-none">&rarr;</span>
    <span class="text-[12px] font-semibold">keep the decoder</span>
  </div>
</div>

</div>

---
layout: section
routeAlias: part-2-training
---

# Part 2: Three-Stage Training

<div class="text-2xl mt-8 opacity-80">
From <b>pre-training</b> to <b>post-training</b>
</div>



---
routeAlias: stage-1-pretraining
---

# Autoregressive next-token prediction

<style>
@keyframes flowInput {
  0% {
    left: 50px;
    opacity: 1;
    transform: translateY(-50%) scale(1);
  }
  35% {
    left: 350px;
    opacity: 0.6;
    transform: translateY(-50%) scale(0.7);
  }
  50% {
    left: 380px;
    opacity: 0;
    transform: translateY(-50%) scale(0.5);
  }
  51% {
    opacity: 0;
  }
  100% {
    opacity: 0;
  }
}

@keyframes flowOutput {
  0% {
    left: 450px;
    opacity: 0;
    transform: translateY(-50%) scale(0.5);
  }
  50% {
    left: 450px;
    opacity: 0;
  }
  65% {
    left: 520px;
    opacity: 0.6;
    transform: translateY(-50%) scale(0.7);
  }
  100% {
    left: 600px;
    opacity: 1;
    transform: translateY(-50%) scale(1);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.5);
  }
}

.transformer-box {
  animation: pulse 2s ease-in-out infinite;
}

.flow-input {
  position: absolute;
  top: 50%;
  animation: flowInput 4s ease-in-out infinite;
  pointer-events: none;
}

.flow-output {
  position: absolute;
  top: 50%;
  animation: flowOutput 4s ease-in-out infinite;
  pointer-events: none;
}
</style>

<div class="relative flex items-center justify-center mt-12">

<div class="flex items-center gap-8">

<div class="text-center">
<div class="text-lg font-semibold mb-2">Input Sequence</div>
<div class="p-4 bg-gray-100 rounded-lg">
<div class="flex gap-2">
<span class="px-3 py-2 bg-blue-200 rounded text-sm">The</span>
<span class="px-3 py-2 bg-blue-200 rounded text-sm">cat</span>
<span class="px-3 py-2 bg-blue-200 rounded text-sm">sat</span>
<span class="px-3 py-2 bg-blue-200 rounded text-sm">on</span>
<span class="px-3 py-2 bg-blue-200 rounded text-sm">the</span>
</div>
</div>
</div>

<div class="text-5xl text-gray-400"></div>

<div class="text-center relative z-10">
<div class="text-lg font-semibold mb-2">Transformer</div>
<div class="transformer-box w-40 h-40 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center text-white text-3xl font-bold">
<img src="/figs/network.png" class="w-24 h-24" />
</div>
</div>

<div class="text-5xl text-gray-400"></div>

<div class="text-center">
<div class="text-lg font-semibold mb-2">Probability Distribution</div>
<div class="p-4 bg-gray-100 rounded-lg text-sm w-64">
<div class="flex items-center gap-2 mb-2">
<span class="w-16 text-right font-semibold">mat:</span>
<div class="flex-1 bg-gray-200 rounded h-5 overflow-hidden">
<div class="h-full bg-green-500 rounded animate-pulse" style="width: 85%;"></div>
</div>
<span class="text-xs font-semibold">85%</span>
</div>
<div class="flex items-center gap-2 mb-2">
<span class="w-16 text-right">table:</span>
<div class="flex-1 bg-gray-200 rounded h-5 overflow-hidden">
<div class="h-full bg-blue-400 rounded" style="width: 10%;"></div>
</div>
<span class="text-xs">10%</span>
</div>
<div class="flex items-center gap-2 mb-2">
<span class="w-16 text-right">floor:</span>
<div class="flex-1 bg-gray-200 rounded h-5 overflow-hidden">
<div class="h-full bg-gray-400 rounded" style="width: 3%;"></div>
</div>
<span class="text-xs">3%</span>
</div>
<div class="flex items-center gap-2">
<span class="w-16 text-right">other:</span>
<div class="flex-1 bg-gray-200 rounded h-5 overflow-hidden">
<div class="h-full bg-gray-300 rounded" style="width: 2%;"></div>
</div>
<span class="text-xs">2%</span>
</div>
</div>
</div>

</div>

<!-- 流动的输入序列 -->
<div class="flow-input p-3 bg-blue-300 rounded-lg shadow-lg">
<div class="flex gap-1">
<span class="px-2 py-1 bg-blue-400 rounded text-xs text-white">The</span>
<span class="px-2 py-1 bg-blue-400 rounded text-xs text-white">cat</span>
<span class="px-2 py-1 bg-blue-400 rounded text-xs text-white">sat</span>
<span class="px-2 py-1 bg-blue-400 rounded text-xs text-white">on</span>
<span class="px-2 py-1 bg-blue-400 rounded text-xs text-white">the</span>
</div>
</div>

<!-- 流动的输出概率 -->
<div class="flow-output p-3 bg-green-100 rounded-lg shadow-lg w-52">
<div class="space-y-1">
<div class="flex items-center gap-1">
<span class="text-xs w-12">mat:</span>
<div class="flex-1 bg-gray-200 rounded h-3">
<div class="h-full bg-green-500 rounded" style="width: 85%;"></div>
</div>
</div>
<div class="flex items-center gap-1">
<span class="text-xs w-12">table:</span>
<div class="flex-1 bg-gray-200 rounded h-3">
<div class="h-full bg-blue-400 rounded" style="width: 10%;"></div>
</div>
</div>
<div class="flex items-center gap-1">
<span class="text-xs w-12">floor:</span>
<div class="flex-1 bg-gray-200 rounded h-3">
<div class="h-full bg-gray-400 rounded" style="width: 3%;"></div>
</div>
</div>
</div>
</div>

</div>

<div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 text-center">
<p class="text-lg text-gray-600 italic">
Just view Transformer as a box: give it a sequence, <br>
it tells you the probability of each token in the vocabulary being next.
</p>
</div>



---


# Training Pipeline (Three Stages)

<style scoped>
.slidev-code {
  font-size: 1.5em !important;
}
.slidev-code .line {
  line-height: 1.6 !important;
}
</style>

````md magic-move
```python
"""
═══════════════════════════════════════════════════════
Step 1: Pre-training (Data Preparation)
First we collect massive text corpora from various sources
such as Wikipedia, Books, and code repositories
═══════════════════════════════════════════════════════
"""

data = load_corpus([
    "CommonCrawl",   # Web pages
    "Wikipedia",     # Knowledge base
    "Books",         # Literature
    "Code",          # Programming
    "Academic"       # Research papers
])

tokenized_data = tokenize(data)  # Tokenize and clean

data_example = [
    {
      "Neural networks are a class of machine learning ..."
    },
]

```

```python
"""
═══════════════════════════════════════════════════════
Step 1: Pre-training (Training)
With those data we use autoregressive next-token prediction
Train the model to predict the next token at each position
═══════════════════════════════════════════════════════
"""

model = Transformer(
    vocab_size=50000,
    hidden_size=4096,
    num_layers=32,
    num_heads=32
)

for batch in tokenized_data:
    logits = model(batch.input)  # Forward pass
    loss = cross_entropy(logits, batch.target)  # Compute loss
    
    loss.backward()  # Backpropagation
    optimizer.step()  # Update weights

```

```python
"""
═══════════════════════════════════════════════════════
Step 2: Supervised Fine-Tuning (SFT)
Use high-quality human-written instruction-response pairs
to teach the model to follow instructions
═══════════════════════════════════════════════════════
"""

instruction_data = [
    {
        "input": "Explain neural networks",
        "output": "Neural networks are..."
    },
]

for example in instruction_data:
    output = model(example.input)  # Generate response
    loss = cross_entropy(output, example.output)  # Compare with target
    
    loss.backward()
    optimizer.step()

```

```python
"""
═══════════════════════════════════════════════════════
Step 3: Reinforcement Learning (RL)
Use rewards to make the assistant more helpful, safe,
or correct beyond simply imitating demonstrations
═══════════════════════════════════════════════════════
"""

RL_data = [{ "prompt": "Explain neural networks to a beginner"},]
ref_model = copy(model)  # Frozen SFT model for KL control
reward_fn = choose_reward_source(
    human_preference_model=reward_model,  # RLHF
    rule_based_verifier=verifier          # RLVR
)
for prompt in rl_prompts:
    responses = model.generate(prompt, n)
    rewards = [reward_fn(prompt, r) for r in responses]
    advantages = normalize(rewards)  # Good answers go up
    loss = policy_gradient_loss(model, responses, advantages, beta * kl_divergence) 
    
    loss.backward()
    optimizer.step()

```

```python
"""
══════════════════════════════════════════════════════════════════════════════════════════
Result - A model that follows instructions and optimizes for rewarded behavior
══════════════════════════════════════════════════════════════════════════════════════════
"""
# Before SFT:
input = "Neural networks are"
output = "Neural networks are a class of machine learning [continues with raw text]"
# After SFT:
input = "Explain neural networks"
output = """
Neural networks are computational models inspired by 
the human brain. They consist of:
1. Input layer - receives data
2. Hidden layers - process information ...
"""
# After RL:
input = "Explain neural networks to a beginner"
output = """
Neural networks are pattern-learning systems. 
They learn by example and improves by adjusting themselves based on errors
"""
```
````


---
layout: section
---

# Pre-training &amp; Supervised Fine-Tuning

<div class="text-xl mt-8 opacity-80">
<b>Pre-training</b> provides the foundation; <b>supervised fine-tuning</b> turns it into an instruction-following model.
</div>

---



# Training Objective: Minimize Surprise

<div class="grid grid-cols-2 gap-8">

<div>

### Training Data:

$\mathcal{D} = \{x_i\}_{i=1}^N$  

Each $x_i = (x_1, \ldots, x_T)$ is a token sequence.

</div>

<div>

### Autoregressive factorization：

$$P_\theta(x_{1:T}) = \prod_{t=1}^{T} P_\theta(x_t \mid x_{\lt t})$$

The causal mask prevents the model from peeking at future tokens.

</div>

</div>

<div class="mt-3 p-4 pt-3 pb-0 bg-gradient-to-r from-blue-50 to-purple-50 border-5 border-blue-300 rounded-lg">

### Training Goal
$$\max_\theta \prod_{t=1}^{T} P_\theta(x_t \mid x_{<t})$$
We want the model to assign as much probability as possible to the correct token $x_t$ at position $t$

</div>

---

# Cross-Entropy: The Surprise Meter

<div class="grid grid-cols-2 gap-4 mt-3 text-[0.96em]">

<div>

### One position

If the true next token is <b>mat</b>, the target distribution is one-hot:

<div class="mt--3 space-y-1.5 text-sm">
<div class="flex items-center gap-2"><span class="w-16 font-semibold">mat</span><div class="h-5 bg-green-500 rounded" style="width: 200px;"></div><span>target = 1</span></div>
<div class="flex items-center gap-2"><span class="w-16">table</span><div class="h-5 bg-gray-300 rounded" style="width: 30px;"></div><span>target = 0</span></div>
<div class="flex items-center gap-2"><span class="w-16">floor</span><div class="h-5 bg-gray-300 rounded" style="width: 20px;"></div><span>target = 0</span></div>
</div>

**Model distribution** $p_t$: softmax output over vocabulary $|V|$

</div>

<div>


### 

At position $t$:

<div class="text-sm mt--3">

$$H(q_t, p_t) = -\sum_{v=1}^{|V|} q_t(v) \log p_t(v)$$

</div>

Since $q_t$ is one-hot:

<div class="text-sm mt--3">

$$H(q_t, p_t) = -\log p_t(x_t)$$

</div>

This is also the **Negative Log-Likelihood (NLL)**

</div>

</div>

<div class="mt--3 px-4 pt-1 pb-0 bg-blue-50 border-5 border-blue-200 rounded-lg">

### Loss for Entire Sequence
<div class="text-m">

$$\mathcal{L}(\theta) = \sum_{i=1}^{N}\sum_{t=1}^{T} -\log p_\theta(x_{i,t} \mid x_{i,<t})$$
</div>

In practice: average over **batch** and over **tokens** to get the training loss

</div>

---
routeAlias: stage-2-sft
---

# SFT: From Base Model to Assistant

<div class="grid grid-cols-2 gap-6 mt-5">

<div class="p-5 bg-slate-50 border-2 border-slate-300 rounded">
<div class="text-xl font-bold mb-3">Pre-training: learn the world</div>
<div class="space-y-3 text-base">
<div><b>Data:</b> massive unlabeled text</div>
<div><b>Loss:</b> all next-token positions</div>
<div><b>Behavior:</b> continue whatever distribution the prompt resembles</div>
</div>
</div>

<div class="p-5 bg-purple-50 border-2 border-purple-300 rounded">
<div class="text-xl font-bold mb-3">SFT: learn the interface</div>
<div class="space-y-3 text-base">
<div><b>Data:</b> instruction-response demonstrations</div>
<div><b>Loss:</b> assistant response tokens only</div>
<div><b>Behavior:</b> answer in the desired role, style, and format</div>
</div>
</div>

</div>


<div class="mt-3">

## SFT Loss Masking

<div class="flex flex-col gap-4 mt-2">

<div class="flex items-center gap-4">
<div class="w-32 text-sm font-semibold text-blue-600">input_ids</div>
<div class="flex gap-1">
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-red-200 border-2 border-red-400 rounded flex items-center justify-center text-xs">user</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>
<div class="w-12 h-12 bg-green-200 border-2 border-green-400 rounded flex items-center justify-center text-xs">asst</div>

</div>
</div>

<div class="flex items-center gap-4">
<div class="w-32 text-sm font-semibold text-purple-600">labels</div>
<div class="flex gap-1">
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-gray-200 border-2 border-gray-400 rounded flex items-center justify-center text-xs relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-transparent via-gray-400 to-transparent opacity-30" style="background: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(0,0,0,0.1) 5px, rgba(0,0,0,0.1) 10px);"></div>
<span class="relative z-10">-100</span>
</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
<div class="w-12 h-12 bg-blue-300 border-2 border-blue-500 rounded flex items-center justify-center text-xs font-semibold">ID</div>
</div>
</div>

<div class="flex gap-6 justify-center mt-4 text-sm">
<div class="flex items-center gap-2">
<div class="w-8 h-8 bg-red-200 border-2 border-red-400 rounded"></div>
<span><b>User:</b> Input prompt (ignored in loss)</span>
</div>
<div class="flex items-center gap-2">
<div class="w-8 h-8 bg-green-200 border-2 border-green-400 rounded"></div>
<span><b>Assistant:</b> Target response</span>
</div>
<div class="flex items-center gap-2">
<div class="w-8 h-8 bg-blue-300 border-2 border-blue-500 rounded"></div>
<span><b>Labels:</b> Actual token IDs (for loss)</span>
</div>
</div>

<div class="mt-3 text-xs text-gray-600 text-center">
Label = -100 means "ignore this token in loss computation" (PyTorch convention)
</div>

</div>

</div>

---
---

# SFT Training Mechanism

<SFTLossFlowAnimation />

---
layout: section
routeAlias: stage-3-rlhf
---

# Reinforcement Learning from Human Feedback

<div class="text-xl mt-8 opacity-80">
<b>Preference optimization and RLHF</b> teach the model to better follow human preferences.
</div>

---


# Reinforcement Learning

<div class="flex justify-center items-center mt--3">
<img src="/figs/sdm.png" class="w-4.2/5" />
</div>


---

# Reinforcement learning from human feedback (RLHF)


<div class="flex justify-center items-center mt-7">
<img src="/figs/RLHFpapers.png" class="w-5/5" />
</div>


---

# Reward learning in RLHF
<div class="flex justify-center items-center mt-7">
<img src="/figs/reward.png" class="w-5/5" />
</div>

---

# Preference Data Example

**Prompt:** *Explain quantum computing to a 10-year-old*

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="p-4 border-2 border-green-500 rounded">

### Response A (Chosen) ✓

"Imagine a super-fast computer that can 
try many answers at once, like having 
multiple copies of yourself doing homework 
simultaneously!"

**Why chosen:**
- Age-appropriate language
- Good analogy
- Engaging tone

</div>

<div class="p-4 border-2 border-red-500 rounded">

### Response B (Rejected) ✗

"Quantum computing leverages quantum 
mechanical phenomena such as superposition 
and entanglement to perform computations..."

**Why rejected:**
- Too technical
- Not age-appropriate
- Jargon-heavy

</div>

</div>

---

# Reward learning in RLHF(Cont'd)
<div class="flex justify-center items-center mt-15">
<img src="/figs/rewardlearning.png" class="w-5/5" />
</div>

---

# Small example of BT model 
<div class="flex justify-center items-center mt-5">
<img src="/figs/btexample.png" class="w-5/5" />
</div>

---


# RLHF Stage: Reward Model Training

<div class="grid grid-cols-2 gap-4">

<div>

## Collecting Preferences

1. Give prompt to model
2. Generate multiple responses (A, B)
3. Humans choose better one
4. Create pairwise comparisons

<div class="space-y-4 text-sm mt-7" >
</div>


## Training Objective

$$
\mathcal{L}_{\text{RM}} = -\mathbb{E}\left[\log\sigma(r_{\text{RM}}(x,y^+) - r_{\text{RM}}(x,y^-))\right]
$$

- $y^+$: chosen response
- $y^-$: rejected response


</div>

<div>

```python
# Reward Model Training
def train_reward_model(preferences):
    reward_model = RewardModel()
    
    for (prompt, chosen, rejected) in preferences:
        # Compute rewards
        r_chosen = reward_model(prompt, chosen)
        r_rejected = reward_model(prompt, rejected)
        
        # Bradley-Terry loss
        loss = -log(
            sigmoid(r_chosen - r_rejected)
        )
        
        loss.backward()
        optimizer.step()
    
    return reward_model
```

</div>

</div>

---

# Algorithm I: PPO-based approach 
<div class="text-right text-sm mt--10 mr-20">
(Proximal Policy Optimization)
</div>
<div class="flex justify-center items-center mt-5">
<img src="/figs/InstructGPT.png" class="w-4/5" />
</div>
<div class="text-right text-sm mt-2 mr-8">
- from InstructGPT (Ouyang et al., 2022)
</div>

---

# PPO Training Loop 

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

### Key Components

<div class="space-y-4 text-sm mt-3" >

#### 1) Policy Model $\pi_\theta$

The LLM we update (the "actor")

#### 2) Reward Model $r_{\text{RM}}(x, y)$

Scores a response $y$ given prompt $x$


#### 3) Value Model $V_\phi(x)$

The baseline we use to calculate the advantage function to stabilize training

#### 4) Reference policy  $\pi_{\text{ref}}$

To prevent reward hacking / distribution shift by KL penalty:

<div class="text-xs">

$$r_{\text{final}} = r_{\text{RM}}(x, y) - \beta \cdot KL(\pi_\theta(\cdot \mid x) \| \pi_{\text{ref}}(\cdot \mid x))$$

</div>


</div>

</div>

<div>

<div class="flex justify-center items-center mt-0">

```python
def rlhf_training(policy_model,reward_model,value_model,prompts):
    ref_policy = freeze(copy(policy_model)) 
    for step in range(num_steps):
        experiences = []
        for prompt in prompts:
            # Generate response
            response = policy_model.generate(prompt)
            # Get reward from reward model
            reward = reward_model(prompt, response)
            logp_old = policy_model.logprob(prompt, response)
            # Add KL penalty (stay close to reference policy)
            kl_penalty = kl_divergence(policy_model, ref_policy)
            final_reward = reward - beta * kl_penalty
            experiences.append((prompt, response, 
            final_reward, logp_old))
            # Advantage (usually estimated by GAE)
            adv = compute_advantages(experiences, value_model)
            experiences.append(adv)
        # PPO update
        for _ in range(ppo_epochs):
            ppo_step(policy_model, experiences)
    return policy_model
```

</div>

</div>

</div>

---

# PPO Training Loop(Cont'd)

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

## PPO Step

**Key Idea:** improve the policy, but **avoid large destructive updates**.

**Objective:**

<div class="text-sm">

$$
L^{\text{CLIP}}(\theta) = \mathbb{E}\left[\min(\rho_t\hat{A}_t, \text{clip}(\rho_t, 1-\epsilon, 1+\epsilon)\hat{A}_t)\right]
$$

</div>

where:
- $\rho_t = \frac{\pi_\theta(y_t \mid x,y_{<t})}{\pi_{\text{old}}(y_t \mid x,y_{<t})}$ (importance sampling ratio)
- $\hat{A}_t \thickapprox Q(x,y_{\le t}) - V_\phi(x,y_{<t})$ (token-level advantage)
- $\epsilon$  (clip parameter)

</div>

<div>

```python
# PPO Update
def ppo_step(policy, value_model, experiences):
    for (contexts, tokens, advs, old_logps, values_old) in experiences:
        # Probability ratio
        new_logps = policy.log_prob(contexts, tokens)
        ratios = exp(new_logps - old_logps)
        
        # loss of the policy
        surr1 = ratios * advs
        surr2 = clip(ratios, 1-eps, 1+eps) * advs
        policy_loss = -mean(min(surr1, surr2))

        # loss of the value model
        values_new = value_model(contexts)
        returns = advs + values_old
        value_loss = mean((values_new - returns)**2)

        loss = policy_loss + c_v * value_loss
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

</div>

</div>

---

# Policy Gradient and PPO Surrogate

<div class="text-[18px] leading-snug mt-4">

### The objective

$$
J(\theta)
=
\mathbb{E}_{x\sim\mathcal D,\,y\sim\pi_\theta(\cdot\mid x)}
\left[
r(x,y)
\right]
$$

<div class="mt-6 border-2 border-blue-300 bg-blue-50 px-5 py-4 rounded text-[17px]">

The model samples a discrete response $y$, so the sample operation itself is not differentiable.
Policy gradient gives us a gradient estimator that avoids backpropagating through the sample.
</div>

<div class="mt-6">

If the response space were tiny, we could enumerate all possible $y$:

$$
J(\theta)
=
\mathbb{E}_{x\sim\mathcal D}
\left[
\sum_y
\pi_\theta(y\mid x)r(x,y)
\right]
$$

</div>

</div>

---

# Policy Gradient: Why the Trick Is Needed

<div class="text-[18px] leading-snug mt-4">

For language models, the response space is enormous, so training should use Monte Carlo samples:

$$
x\sim\mathcal D,
\qquad
y\sim\pi_\theta(\cdot\mid x)
$$

However the sample $y$ is a discrete token sequence and we cannot directly differentiate through the act of sampling it.

<div class="mt-6">

Start from the enumerable form and differentiate the probability mass:

$$
\begin{aligned}
J(\theta)
&=
\mathbb{E}_{x\sim\mathcal D}
\left[
\sum_y
\pi_\theta(y\mid x)r(x,y)
\right] \\
\nabla_\theta J(\theta)
&=
\mathbb{E}_{x\sim\mathcal D}
\left[
\sum_y
\nabla_\theta \pi_\theta(y\mid x)r(x,y)
\right]
\end{aligned}
$$

</div>

</div>

---

# Policy Gradient: Log-Derivative Trick

<div class="text-[17px] leading-tight mt-3">

Rewrite the derivative of the probability using:

$$
\nabla_\theta \pi_\theta(y\mid x)
=
\pi_\theta(y\mid x)
\nabla_\theta \log\pi_\theta(y\mid x)
$$

This turns the gradient into an expectation over sampled responses:

$$
\begin{aligned}
\nabla_\theta J(\theta)
&=
\mathbb{E}_{x\sim\mathcal D}
\left[
\sum_y
\pi_\theta(y\mid x)
\nabla_\theta\log\pi_\theta(y\mid x)
r(x,y)
\right] \\
&=
\mathbb{E}_{x\sim\mathcal D,\,y\sim\pi_\theta(\cdot\mid x)}
\left[
\nabla_\theta\log\pi_\theta(y\mid x)r(x,y)
\right]
\end{aligned}
$$

So the on-policy surrogate has the same gradient:

$$
J_{\mathrm{PG}}(\theta)
=
\mathbb{E}_{(x,y)\sim\mathcal{D}}
\left[
\log \pi_\theta(y\mid x)\,r(x,y)
\right]
$$

PPO uses an advantage estimate instead of the raw reward $r(x,y)$ to reduce estimation variance.
</div>

---

# Problem: Our Data Come from an Old Policy

<div class="text-[17px] leading-tight mt-3">

In PPO step (> 1), we collect trajectories with a **frozen snapshot** policy $\pi_{\text{old}}$:

$$\mathcal{D}_{\text{old}} = \{x,y\}, \text{where } x \sim \mathcal D, y \sim \pi_{\text{old}}(\cdot \mid x)$$


If we *naively* plug off-policy data into the policy gradient estimator:

$$\widehat{g}_{\text{naive}} = \mathbb{E}_{(x,y)\sim \mathcal{D}_{\text{old}}}\Big[\nabla_\theta \log \pi_\theta(y\mid x)\; A(x,y)\Big]$$

<div class="mt-10 p-4 bg-red-50 border-2 border-red-300 rounded-lg">
<div class="text-red-700 font-bold">⚠️ This is generally <span class="text-xl">biased</span></div>

Because the expectation is taken under $\pi_{\text{old}}$ rather than $\pi_\theta$:

$$\widehat{g}_{\text{naive}} \neq \nabla_\theta J(\theta)$$
</div>



</div>

---

# Fix: Importance Sampling (IS)

<div class="text-base">

**What we want:** Use $\mathcal{D}_{\text{old}}$ to estimate $\nabla_\theta J(\theta)$

**Key insight — Importance weighted gradient:**

$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \sum_{y} \pi_\theta(y\mid x)\,\nabla_\theta \log \pi_\theta(y\mid x)\,A(x,y) \\
&= \sum_{y}\left[\frac{\pi_\theta(y\mid x)}{\pi_{\text{old}}(y\mid x)}\nabla_\theta \log \pi_\theta(y\mid x)\,A(x,y)\, \pi_{\text{old}}(y\mid x)\right] \\
&= \sum_{y}\left[\frac{\nabla_\theta\pi_\theta(y\mid x)}{\pi_{\text{old}}(y\mid x)}A(x,y)\, \pi_{\text{old}}(y\mid x)\right] \\
&= \mathbb{E}_{y\sim \mathcal{D}_{\text{old}}}\left[\frac{\nabla_\theta \pi_\theta(y\mid x)}{\pi_{\text{old}}(y\mid x)}\, A(x,y)\right]
\end{aligned}
$$

**PPO surrogate objective:**

$$L(\theta) = \mathbb{E}_{(x,y)\sim \mathcal{D}_{\text{old}}}\left[\frac{ \pi_\theta(y\mid x)}{\pi_{\text{old}}(y\mid x)}\, A(x,y)\right]$$




</div>




---

# PPO Pipeline Overview

<div class="flex justify-center items-center mt-7">
<img src="/figs/ppo_pipeline_003.png" style="width: 110%; max-height: 550px; object-fit: contain;" />
</div>

---


# Algorithm II: DPO-based approach
<div class="text-right text-sm mt--10 mr-10">
(Direct Preference Optimization)
</div>
<div class="flex justify-center items-center mt-15">
<img src="/figs/DPO.png" class="w-5/5" />
</div>

---

# DPO: Training Loop

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

### Key Components

<div class="space-y-4 text-sm mt-3">

#### 1) Policy Model $\pi_\theta$

The LLM we optimize directly

#### 2) Reference Model $\pi_{\text{ref}}$

Frozen copy of initial SFT model

#### 3) Preference Data

Pairs of $(x, y^+, y^-)$ where:
- $x$: prompt
- $y^+$: preferred (chosen) response
- $y^-$: rejected response

**Key Difference:** No separate reward model needed!

</div>

</div>

<div>

### DPO Training Loop

<div class="space-y-3 text-sm">

#### 1. Sample Preference Pair

Get $(x, y^+, y^-)$ from preference dataset

#### 2. Compute Implicit Rewards

<div class="text-xs">

$$r_\theta(x, y) + C(x) = \beta \log \frac{\pi_\theta(y\mid x)}{\pi_{\text{ref}}(y\mid x)} $$

</div>

#### 3. DPO Loss

<div class="text-xs">

$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}_{(x,y^+,y^-)} \left[\log \sigma\left(\beta \log \frac{\pi_\theta(y^+\mid x)}{\pi_{\text{ref}}(y^+\mid x)} - \beta \log \frac{\pi_\theta(y^-\mid x)}{\pi_{\text{ref}}(y^-\mid x)}\right)\right]$$

</div>

#### 4. Update Policy

Gradient descent on $\mathcal{L}_{\text{DPO}}$ to update $\pi_\theta$

</div>

</div>

</div>

---

# DPO Derivation: Setup

<div class="text-[21px] leading-normal mt-4">

### Preference data:

$$
\mathcal{D}=\{(x^{(i)},y^{+(i)},y^{-(i)})\}_{i=1}^{N},
\qquad
y^+\succ y^- \mid x
$$

### KL-regularized RLHF objective:

$$
\max_{\pi}\;
\mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi(y\mid x)}
\left[r(x,y)\right]
-\beta\,
\mathbb{D}_{\mathrm{KL}}
\left[
\pi(y\mid x)\,\|\,\pi_{\text{ref}}(y\mid x)
\right]
$$

### DPO purpose:

<div class="text-[18px] leading-snug mt-3">
Find an objective function that directly optimizes for the policy best satisfying the preferences with a simple classification
objective, without fitting a reward model first, and then use RL to find a policy that maximizes the learned reward.
</div>

</div>

---

# DPO Derivation: Objective Transformation

<div class="text-[15px] leading-snug mt-1">

Under any reward function $r(x,y)$, reference model $\pi_{\mathrm{ref}}$ and a general non-parametric policy class, we have

</div>


$$
\begin{aligned}
&\max_{\pi}\;\mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi}\!\Big[r(x,y)\Big]
-\beta\,\mathbb{D}_{\mathrm{KL}}\!\Big(\pi(y|x)\,\|\,\pi_{\mathrm{ref}}(y|x)\Big) \\
&=\max_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\mathbb{E}_{y\sim\pi(\cdot|x)}
\Big[r(x,y)-\beta\log\frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)}\Big] \\
&=\min_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\mathbb{E}_{y\sim\pi(\cdot|x)}
\Big[\log\frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)}-\frac{1}{\beta}r(x,y)\Big] \\
&=\min_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\mathbb{E}_{y\sim\pi(\cdot|x)}
\Big[\log\frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)\exp\!\big(\frac{1}{\beta}r(x,y)\big)}\Big]
\end{aligned}
$$


<div class="text-[15px] leading-snug mt-1">

  Gibbs' inequality tells us that the KL divergence is minimized at 0 if and only if the
  two distributions are identical. Following this observation, we can reformulate the
  optimization problem as finding a policy $\pi'$ that transforms the objective into the following form:

</div>

$$
\begin{aligned}
\min_{\pi}\;
\mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi}
\left[
\mathbb{D}_{\mathrm{KL}}
\left(\pi(y\mid x)\,\|\,\pi^{'}(y\mid x)\right)
-C(x)
\right]
\end{aligned},
\quad
\text{where } C(x) \text{ does not depend on } \pi
$$

---

# DPO Derivation: Partition Function

<div class="text-[17px] leading-snug mt-4">

Here, $\pi'$ should be independent of the current policy $\pi$, while still defining a valid probability distribution. Specifically, it must satisfy
$$
\pi'(y \mid x) \geq 0 \quad \text{for all } y,
\qquad
\sum_y \pi'(y \mid x) = 1.
$$
To ensure normalization, we define the partition function
$$
Z(x)
=
\sum_y
\pi_{\text{ref}}(y \mid x)
\exp\left(\frac{1}{\beta} r(x,y)\right), \text{and get } \pi'(y \mid x)
=
\frac{1}{Z(x)}
\pi_{\text{ref}}(y \mid x)
\exp\left(\frac{1}{\beta} r(x,y)\right),

$$
This gives
$$
\begin{aligned} &\min_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\mathbb{E}_{y\sim\pi(\cdot|x)}
\Big[\log\frac{\pi(y|x)}{\pi_{\mathrm{ref}}(y|x)\exp\!\big(\frac{1}{\beta}r(x,y)\big)}\Big] \\ &=\min_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\mathbb{E}_{y\sim\pi(\cdot|x)} \Big[\log\frac{\pi(y|x)}{\frac{1}{Z(x)}\pi_{\mathrm{ref}}(y|x)\exp\!\big(\frac{1}{\beta}r(x,y)\big)} -\log Z(x)\Big] \end{aligned}
$$
</div>

---

# DPO Derivation: Closed-form Reward

<div class="text-[17px] leading-snug mt-4">
Hence, the optimal policy induced by the reward function can be written as
</div>

$$
\pi_r^{\star}(y \mid x)
=
\pi'(y \mid x)
=
\frac{1}{Z(x)}
\pi_{\mathrm{ref}}(y \mid x)
\exp\left(\frac{1}{\beta} r(x,y)\right).
$$

<div class="text-[17px] leading-snug mt-4">
Rearranging this expression gives the corresponding closed-form reward:
</div>

$$
r(x,y)
=
\beta
\log
\frac{\pi_r^{\star}(y \mid x)}
{\pi_{\mathrm{ref}}(y \mid x)}
+
\beta \log Z(x).
$$

<div class="text-[17px] leading-snug mt-4">

Under the Bradley--Terry preference model, the probability that $y^+$ is preferred over $y^-$ is
</div>

$$
p^{\star}(y^+ \succ y^-  \mid x)
=
\frac{\exp\left(r^{\star}(x,y^+)\right)}
{\exp\left(r^{\star}(x,y^+)\right)
+
\exp\left(r^{\star}(x,y^-)\right)}.
$$

<div class="text-[17px] leading-snug mt-4">
Using the optimal-policy form above, the ground-truth reward can be expressed as
</div>

$$
r^{\star}(x,y)
=
\beta
\log
\frac{\pi^{\star}(y \mid x)}
{\pi_{\mathrm{ref}}(y \mid x)}
+
\beta \log Z(x).
$$

---

# DPO Derivation: DPO Objective


<div class="text-[20px] leading-tight mt-7">

We can formulate a maximum-likelihood objective for a parametrized policy $\pi_\theta$.
Analogous to the reward-modeling objective, the policy objective becomes
</div>
<div class="text-[16px] leading-tight mt-20">
  
</div>
$$
\mathcal{L}_{\mathrm{DPO}}(\pi_{\theta};\pi_{\mathrm{ref}})
=
-
\mathbb{E}_{(x,y^+,y^-)\sim\mathcal{D}}
\left[
\log
\sigma
\left(
\beta
\log
\frac{\pi_{\theta}(y^+ \mid x)}
{\pi_{\mathrm{ref}}(y^+ \mid x)}
-
\beta
\log
\frac{\pi_{\theta}(y^- \mid x)}
{\pi_{\mathrm{ref}}(y^- \mid x)}
\right)
\right].
$$
<div class="text-[16px] leading-tight mt-20">
  
</div>
<div class="text-[20px] leading-tight mt-7">

In this way, DPO fits an implicit reward through an alternative parameterization, whose optimal policy is directly represented by $\pi_\theta$.
</div>
---

# DPO training pipeline

<div class="flex justify-center items-center mt-3">
<img src="/figs/dpo-logprob-flow.png" style="width: 98%; max-height: 470px; object-fit: contain;" />
</div>

---

# DPO vs PPO


<div class="flex justify-center items-center mt-3">
<img src="/figs/ppovsdpo.png" class="w-4.8/5" />
</div>

---

# RLHF Challenges and Solutions

<div class="grid grid-cols-2 gap-8 mt-4">

<div>

## Challenges

<div class="space-y-4 text-sm">

#### 1. Reward\Preference Model Limitations
Can't capture all preferences

#### 2. Training Instability
- PPO sensitive to reward model
- DPO sensitive to reference policy

#### 3. Reward Hacking
Model exploits reward model weaknesses

#### 4. Expensive Human Feedback
Requires thousands of comparisons



</div>

</div>

<div>

## Advanced Solutions

<div class="space-y-4 text-sm">

#### VRPO (Variance-Reduced Preference Optimization)
**Paper:** *Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning*

- An auxiliary preference model to capture human preferences
- Variance reduction and policy improvement


#### DRPO (Doubly Robust Preference Optimization)
**Paper:** *Doubly Robust Alignment for Large Language Models*

- Doubly robust and efficient estimator for preference evaluation
- Doubly robust preference optimization for LLM fine-tuning


</div>

</div>

</div>

---

# Robust RLHF For LLMs Fine-tuning

<div class="flex justify-center mt-2">
<img src="/figs/vrpo.png" class="w-[72%] h-[245px] object-contain" />
</div>

<div class="mt-2 pt-2 border-t border-slate-300">
<MathTex display tex="\begin{aligned} m_{\eta,\theta}(x,y^{(1)},y^{(2)})&=\sum_{u=0}^{1}\ell(x,y^{(1)},y^{(2)},u;\theta)\,p_\eta(u\mid x,y^{(1)},y^{(2)}),\\[2pt] \widetilde{\mathcal L}_{\mathrm{VRPO}}(\theta)&=\mathbb E_{\mathcal D}\!\left[\ell_\theta-m_{\eta,\theta}\right]+\mathbb E_{x,\,\widetilde y^{(1)},\widetilde y^{(2)}\sim\pi_{\mathrm{ref}}}\!\left[m_{\eta,\theta}(x,\widetilde y^{(1)},\widetilde y^{(2)})\right]. \end{aligned}" class="text-[0.55em]" />
<div class="mt-1 text-[12px] leading-5 text-slate-700"><b>Control-variate idea:</b> subtract the auxiliary model's prediction on labeled pairs, then add back its expectation under the reference policy. With a correctly specified reference policy, the mean is preserved while variance falls when <MathTex tex="p_\eta" /> is informative.</div>
</div>

<div class="mt-1 text-[9px] text-slate-500">Ye, Zhou, Zhu, Quinzan, and Shi (2025), <i>Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning</i>, arXiv:2504.03784.</div>

---

# DRPO: Doubly Robust Preference Optimization

<div class="flex justify-center mt-2">
<img src="/figs/drpo.png" class="w-[92%] h-[250px] object-contain" />
</div>

<div class="mt-2 pt-2 border-t border-slate-300">
<MathTex display tex="\begin{aligned} \rho_a(x)&=\frac{\pi_\theta(y^{(a)}\mid x)}{\widehat\pi_{\mathrm{ref}}(y^{(a)}\mid x)},\\[-1pt] \psi_{\mathrm{DR}}&=\frac12\sum_{a=1}^{2}\left\{\mathbb E_{\widetilde y\sim\pi_\theta(\cdot\mid x)}\widehat g(x,\widetilde y,y^{(a)})+(-1)^{a-1}\rho_a(x)\left[z-\widehat g(x,y^{(1)},y^{(2)})\right]\right\},\\[-1pt] \widehat\pi&=\arg\max_{\pi_\theta}\left\{\mathbb E_{\mathcal D}[\psi_{\mathrm{DR}}]-\beta\,\mathbb E_xD_{\mathrm{KL}}(\pi_\theta(\cdot\mid x)\,\|\,\widehat\pi_{\mathrm{ref}}(\cdot\mid x))\right\}. \end{aligned}" class="text-[0.49em]" />
<div class="mt-1 text-[12px] leading-5 text-slate-700"><MathTex tex="z\in\{0,1\}" /> is the observed preference label. The direct prediction <MathTex tex="\widehat g" /> is augmented by an importance-weighted residual; consistency requires either <MathTex tex="\widehat g" /> or <MathTex tex="\widehat\pi_{\mathrm{ref}}" /> to be correctly specified.</div>
</div>

<div class="mt-1 text-[9px] text-slate-500">Xu, Ye, Zhou, Zhu, Quinzan, and Shi (2025), <i>Doubly Robust Alignment for Large Language Models</i>, arXiv:2506.01183.</div>

---
layout: section
routeAlias: part-3-reasoning
---

# Stage 3: Reasoning &amp; RLVR

<div class="text-xl mt-8 opacity-80">
<b>Reasoning and RLVR</b> further improve the model’s ability to solve complex or verifiable tasks.
</div>

---
routeAlias: inference-time-reasoning
---

# Reasoning: Make Intermediate Steps Explicit

<div class="mt-2 px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-[12px] text-slate-700">
Instead of jumping directly to a final answer, the model generates a sequence of intermediate steps that lead to the solution.
</div>

<div class="mt-4 px-4 py-3 rounded-2xl border-2 border-orange-200 bg-white shadow-sm">
<img src="/figs/reasoning-elephant.png" class="w-full max-h-[245px] object-contain" />
</div>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="px-4 py-3 rounded-xl border-2 border-slate-200 bg-slate-50">
<div class="flex items-center justify-between"><div class="text-[10px] uppercase tracking-[0.14em] font-bold text-slate-500">Direct generation</div><span class="px-2 py-0.5 rounded-full bg-white border border-slate-200 text-[9px] text-slate-500">final answer only</span></div>
<MathTex display tex="x\longrightarrow y" class="text-[0.90em] mt-1" />
</div>
<div class="px-4 py-3 rounded-xl border-2 border-emerald-200 bg-emerald-50">
<div class="flex items-center justify-between"><div class="text-[10px] uppercase tracking-[0.14em] font-bold text-emerald-700">Reasoning trajectory</div><span class="px-2 py-0.5 rounded-full bg-white border border-emerald-200 text-[9px] text-emerald-700">steps become context</span></div>
<MathTex display tex="x\longrightarrow\underbrace{y_1\longrightarrow y_2\longrightarrow\cdots\longrightarrow y_T}_{\text{response }y}" class="text-[0.78em] mt-1" />
</div>
</div>

<div class="mt-3 flex items-center justify-between text-[10px] text-slate-500">
<span>Intermediate tokens let later tokens condition on the evolving solution path.</span>
</div>

---

# Inference-Time Reasoning: Make the Model Think More

<div class="mt-2 flex items-center gap-3">
<span class="px-3 py-1 rounded-full bg-slate-900 text-white text-[10px] font-bold uppercase tracking-[0.14em]">Representative methods</span>
<span class="text-[11px] text-slate-500">Generate, compare, search, or ground reasoning paths</span>
<div class="h-px flex-1 bg-slate-200"></div>
</div>

<div class="grid grid-cols-2 gap-3 mt-3">

<div class="relative overflow-hidden p-3 rounded-2xl border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-white">
<div class="absolute right-0 top-0 w-16 h-16 rounded-bl-full bg-blue-100/70"></div>
<div class="relative flex items-start justify-between">
<div><div class="text-[9px] font-bold uppercase tracking-[0.14em] text-blue-600">Single path</div><div class="text-lg font-black text-blue-900">Chain-of-Thought</div></div>
<span class="px-2 py-0.5 rounded-full border border-blue-200 bg-white text-[9px] text-blue-700">Wei et al., 2022</span>
</div>
<div class="relative mt-0.5 text-[11px] leading-4 text-slate-600">Generate one explicit reasoning path before the answer.</div>
<div class="relative mt-2 flex items-center justify-center gap-1.5 text-[10px] font-semibold">
<span class="px-2.5 py-1 rounded-lg bg-white border border-blue-200">Prompt</span><span class="text-blue-400">&#8594;</span><span class="px-2.5 py-1 rounded-lg bg-blue-100 text-blue-800">Reasoning path</span><span class="text-blue-400">&#8594;</span><span class="px-2.5 py-1 rounded-lg bg-white border border-blue-200">Answer</span>
</div>
</div>

<div class="relative overflow-hidden p-3 rounded-2xl border-2 border-cyan-200 bg-gradient-to-br from-cyan-50 to-white">
<div class="absolute right-0 top-0 w-16 h-16 rounded-bl-full bg-cyan-100/70"></div>
<div class="relative flex items-start justify-between">
<div><div class="text-[9px] font-bold uppercase tracking-[0.14em] text-cyan-600">Multiple paths</div><div class="text-lg font-black text-cyan-900">Self-Consistency</div></div>
<span class="px-2 py-0.5 rounded-full border border-cyan-200 bg-white text-[9px] text-cyan-700">Wang et al., 2022</span>
</div>
<div class="relative mt-0.5 text-[11px] leading-4 text-slate-600">Sample several reasoning paths and vote over their answers.</div>
<div class="relative mt-2 flex items-center justify-center gap-1 text-[9px] font-semibold">
<span class="px-2 py-1 rounded-lg bg-white border border-cyan-200">Reasoning path 1</span><span class="px-2 py-1 rounded-lg bg-white border border-cyan-200">Reasoning path 2</span><span class="px-2 py-1 rounded-lg bg-white border border-cyan-200">Reasoning path 3</span><span class="text-cyan-500">&#8594;</span><span class="px-2 py-1 rounded-lg bg-cyan-100 text-cyan-800">Vote</span>
</div>
</div>

<div class="relative overflow-hidden p-3 rounded-2xl border-2 border-amber-200 bg-gradient-to-br from-amber-50 to-white">
<div class="absolute right-0 top-0 w-16 h-16 rounded-bl-full bg-amber-100/70"></div>
<div class="relative flex items-start justify-between">
<div><div class="text-[9px] font-bold uppercase tracking-[0.14em] text-amber-600">Deliberate search</div><div class="text-lg font-black text-amber-900">Tree of Thoughts</div></div>
<span class="px-2 py-0.5 rounded-full border border-amber-200 bg-white text-[9px] text-amber-700">Yao et al., 2023</span>
</div>
<div class="relative mt-0.5 text-[11px] leading-4 text-slate-600">Search a tree of partial reasoning paths and recover from poor branches.</div>
<div class="relative mt-2 flex items-center justify-center gap-1.5 text-[10px] font-semibold">
<span class="px-2 py-1 rounded-lg bg-white border border-amber-200">Reasoning prefix</span><span class="text-amber-400">&#8594;</span><span class="px-2 py-1 rounded-lg bg-amber-100 text-amber-800">Branch paths</span><span class="text-amber-400">&#8594;</span><span class="px-2 py-1 rounded-lg bg-white border border-amber-200">Evaluate / backtrack</span>
</div>
</div>

<div class="relative overflow-hidden p-3 rounded-2xl border-2 border-emerald-200 bg-gradient-to-br from-emerald-50 to-white">
<div class="absolute right-0 top-0 w-16 h-16 rounded-bl-full bg-emerald-100/70"></div>
<div class="relative flex items-start justify-between">
<div><div class="text-[9px] font-bold uppercase tracking-[0.14em] text-emerald-600">Reason and act</div><div class="text-lg font-black text-emerald-900">ReAct</div></div>
<span class="px-2 py-0.5 rounded-full border border-emerald-200 bg-white text-[9px] text-emerald-700">Yao et al., 2022</span>
</div>
<div class="relative mt-0.5 text-[11px] leading-4 text-slate-600">Ground each new reasoning segment in actions and observations.</div>
<div class="relative mt-2 flex items-center justify-center gap-1 text-[9px] font-semibold">
<span class="px-2 py-1 rounded-lg bg-white border border-emerald-200">Reasoning</span><span class="text-emerald-400">&#8594;</span><span class="px-2 py-1 rounded-lg bg-emerald-100 text-emerald-800">Action</span><span class="text-emerald-400">&#8594;</span><span class="px-2 py-1 rounded-lg bg-white border border-emerald-200">Observation</span><span class="text-emerald-400">&#8594;</span><span class="px-2 py-1 rounded-lg bg-white border border-emerald-200">Reasoning</span>
</div>
</div>

</div>

<div class="mt-3 px-4 py-2 rounded-xl border border-slate-200 bg-slate-50 flex items-center justify-between">
<div class="text-[12px] text-slate-700">More test-time compute is spent on the <b>reasoning trajectory</b>.</div>
<div class="px-3 py-0.5 rounded-full bg-white border border-slate-300 text-[10px] font-bold text-slate-600">Parameters stay fixed</div>
</div>

---

# Chain-of-Thought Prompting

<div class="mt-2 flex items-center justify-between px-4 py-3 rounded-2xl border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-white">
<div><div class="text-[10px] uppercase tracking-[0.14em] font-bold text-blue-600">Method definition</div><div class="mt-1 text-[13px] text-slate-700">Generate a response <MathTex tex="y" /> that contains intermediate natural-language reasoning before the final answer.</div></div>
<span class="px-3 py-1 rounded-full bg-white border border-blue-200 text-[10px] font-semibold text-blue-700">Wei et al. (2022)</span>
</div>

<div class="grid grid-cols-2 gap-4 mt-3">
<div class="p-3 rounded-xl border border-slate-200 bg-slate-50">
<div class="text-[10px] uppercase tracking-wide font-bold text-slate-500">Standard few-shot exemplar</div>
<div class="mt-2 px-3 py-2 rounded-lg bg-white border border-slate-200 font-mono text-[12px] text-center">&lt;prompt x, response y&gt;</div>
</div>
<div class="p-3 rounded-xl border-2 border-blue-200 bg-blue-50">
<div class="text-[10px] uppercase tracking-wide font-bold text-blue-700">Chain-of-thought exemplar</div>
<div class="mt-2 px-3 py-2 rounded-lg bg-white border border-blue-200 font-mono text-[12px] text-center">&lt;prompt x, response y = reasoning + answer&gt;</div>
</div>
</div>

<div class="mt-3 flex items-center gap-3">
<div class="text-[10px] uppercase tracking-[0.14em] font-bold text-slate-500">Method workflow</div><div class="h-px flex-1 bg-slate-200"></div>
</div>

<div class="grid grid-cols-11 gap-2 mt-2 items-stretch text-center">
<div class="col-span-4 p-3 rounded-xl border-2 border-blue-200 bg-blue-50">
<div class="text-[10px] uppercase tracking-wide font-bold text-blue-700">1 &nbsp; Construct the prompt</div>
<div class="mt-2 space-y-1 text-[10px] font-semibold"><div class="px-2 py-1 rounded bg-white">Prompt <MathTex tex="x_1" /> &#8594; response <MathTex tex="y_1" /></div><div class="px-2 py-1 rounded bg-white">Prompt <MathTex tex="x_2" /> &#8594; response <MathTex tex="y_2" /></div></div>
</div>
<div class="col-span-1 flex items-center justify-center text-2xl text-blue-400">&#8594;</div>
<div class="col-span-2 p-3 rounded-xl border-2 border-amber-200 bg-amber-50 flex flex-col justify-center">
<div class="text-[10px] uppercase tracking-wide font-bold text-amber-700">2 &nbsp; Append</div>
<div class="mt-2 text-sm font-black text-amber-900">New prompt <MathTex tex="x" /></div>
</div>
<div class="col-span-1 flex items-center justify-center text-2xl text-emerald-400">&#8594;</div>
<div class="col-span-3 p-3 rounded-xl border-2 border-emerald-200 bg-emerald-50 flex flex-col justify-center">
<div class="text-[10px] uppercase tracking-wide font-bold text-emerald-700">3 &nbsp; Generate</div>
<div class="mt-2 text-[11px] font-bold"><span class="px-2 py-1 rounded bg-white">Reasoning</span> <span class="text-emerald-500">&#8594;</span> <span class="px-2 py-1 rounded bg-emerald-100">Final answer</span> <span class="text-slate-500">= response <MathTex tex="y" /></span></div>
</div>
</div>

---

# Chain-of-Thought: An Example

<div class="flex items-center gap-2 text-xs">
<span class="px-3 py-1.5 rounded-full bg-amber-100 text-amber-800 font-bold">Zero-shot CoT</span>
<span class="text-slate-500">Same question, same model; only the answer cue changes.</span>
</div>

<div class="mt-3 p-3 rounded-xl border border-slate-200 bg-slate-50">
<div class="text-[10px] uppercase tracking-[0.14em] text-slate-500 font-bold mb-1">Shared question</div>
<div class="text-[13px] leading-5">
A booth earns <b>$50/day</b> from popcorn and <b>3&times; as much</b> from cotton candy for <b>5 days</b>, then pays <b>$30 + $75</b>. What are its net earnings?
</div>
</div>

<div class="grid grid-cols-2 gap-4 mt-3">

<div class="rounded-2xl border-2 border-slate-200 bg-white overflow-hidden">
<div class="px-4 py-2 bg-slate-100 flex items-center justify-between">
<div class="font-bold text-slate-700">Direct prompt</div>
<div class="text-[10px] uppercase tracking-wide text-slate-500">baseline</div>
</div>
<div class="mx-4 mt-3 px-3 py-2 rounded-lg bg-slate-900 text-white font-mono text-[13px]">
Answer: <span class="text-slate-400">_____</span>
</div>
<div class="m-4 p-3 rounded-xl border border-rose-200 bg-rose-50 text-[13px] leading-5">
<div class="text-[10px] uppercase tracking-wide font-bold text-rose-700 mb-1">Illustrative completion</div>
Daily revenue is $50 + $150 = $200. After paying $105, the booth earns <b>$95</b>.
<div class="mt-2 pt-2 border-t border-rose-200 text-rose-800"><b>Failure:</b> the 5-day multiplier is omitted.</div>
</div>
</div>

<div class="rounded-2xl border-2 border-emerald-300 bg-white overflow-hidden shadow-sm">
<div class="px-4 py-2 bg-emerald-100 flex items-center justify-between">
<div class="font-bold text-emerald-800">Chain-of-thought prompt</div>
<div class="text-[10px] uppercase tracking-wide text-emerald-700">one added cue</div>
</div>
<div class="mx-4 mt-3 px-3 py-2 rounded-lg bg-slate-900 text-white font-mono text-[13px]">
Answer: <span class="px-1.5 py-0.5 rounded bg-emerald-500 text-white font-bold">Let's think step by step.</span> <span class="text-slate-400">_____</span>
</div>
<div class="m-4 p-3 rounded-xl border border-emerald-200 bg-emerald-50 text-[13px] leading-5">
<div class="text-[10px] uppercase tracking-wide font-bold text-emerald-700 mb-1">Illustrative completion</div>
Cotton candy earns $50 &times; 3 = $150 per day, so the booth earns $50 + $150 = $200 per day. Over 5 days, its revenue is $200 &times; 5 = $1000. Its total cost is $30 + $75 = $105.
<div class="mt-2 pt-2 border-t border-emerald-200 text-emerald-800"><b>Therefore, the net earnings are $1000 - $105 = $895.</b></div>
</div>
</div>

</div>

<div class="mt-3 px-4 py-2.5 rounded-xl border border-amber-200 bg-amber-50 text-center text-[13px] font-semibold">
The added cue supplies no arithmetic facts; it changes the generated trajectory by making intermediate state explicit.
</div>

<div class="text-[10px] mt-2 text-slate-500">
Zero-shot CoT cue: Kojima et al. (2022). Illustrative completions shown for exposition.
</div>

---

# Self-Consistency: Sample Many Paths, Vote on the Answer

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">

<div class="p-4 border-2 border-cyan-300 rounded bg-cyan-50">
<div class="font-bold text-cyan-700 mb-2">1. Sample</div>
Use temperature to draw multiple chain-of-thought paths.
</div>

<div class="p-4 border-2 border-cyan-300 rounded bg-cyan-50">
<div class="font-bold text-cyan-700 mb-2">2. Extract</div>
Take the final answer from each sampled reasoning path.
</div>

<div class="p-4 border-2 border-cyan-300 rounded bg-cyan-50">
<div class="font-bold text-cyan-700 mb-2">3. Marginalize</div>
Choose the answer that appears most consistently.
</div>

</div>

<div class="mt-8 text-base">

The key idea is not "longer reasoning", but **diverse reasoning**. If several different paths converge to the same answer, that answer is more reliable than a single greedy chain.

</div>

<div class="text-lg mt-6 text-center">

$$
\hat a
=
\arg\max_a \sum_{k=1}^{K}\mathbf{1}\{\mathrm{answer}(y^{(k)})=a\},
\qquad y^{(k)}\sim\pi_\theta(\cdot\mid x)
$$

</div>

---

# Tree of Thoughts: Search Over Intermediate States

<div class="grid grid-cols-2 gap-8 mt-5">

<div>

## From chain to tree

CoT commits to one path:

$$
y_1 \rightarrow y_2 \rightarrow \cdots \rightarrow y_T
$$

ToT keeps multiple partial thoughts alive:

$$
\{y_1^{(1)}, y_1^{(2)}, \ldots\}
\rightarrow
\{y_2^{(1)}, y_2^{(2)}, \ldots\}
$$

</div>

<div>

## Search loop

1. Propose several candidate thoughts.
2. Evaluate whether each partial state is promising.
3. Keep, prune, or backtrack.
4. Continue until a final solution is found.

Useful when early mistakes are costly and backtracking matters.

</div>

</div>

<div class="mt-7 p-4 bg-purple-50 border-l-4 border-purple-500">
ToT treats the LLM as both a generator and a heuristic evaluator inside a search procedure.
</div>

---

# ReAct: Interleave Reasoning and Acting

<div class="grid grid-cols-2 gap-8 mt-5">

<div>

## Reasoning trace

The model writes what it is trying to infer:

<div class="text-sm p-3 bg-green-50 border-l-4 border-green-400">
Thought: I need the current fact before answering.
</div>

## Action trace

The model calls an external tool or environment:

<div class="text-sm p-3 bg-gray-50 border-l-4 border-gray-400">
Action: search / lookup / calculate / query database
</div>

</div>

<div>

## Observation loop

The environment returns information:

<div class="text-sm p-3 bg-yellow-50 border-l-4 border-yellow-400">
Observation: result returned by the tool
</div>

Then the model reasons again, acts again if needed, and eventually answers.

<div class="text-lg mt-6">

$$
\text{Thought} \rightarrow \text{Action} \rightarrow \text{Observation} \rightarrow \text{Thought}
$$

</div>

</div>

</div>

---

# Inference-Time Reasoning: Summary

<div class="mt-3 grid grid-cols-4 gap-3 text-center">
<div class="px-3 py-2.5 rounded-xl border-2 border-blue-200 bg-gradient-to-b from-blue-50 to-white">
<div class="text-base font-black text-blue-900">CoT</div>
<div class="mt-1 text-[10px] font-semibold text-blue-700">prompt &#8594; reasoning path &#8594; answer</div>
</div>
<div class="px-3 py-2.5 rounded-xl border-2 border-cyan-200 bg-gradient-to-b from-cyan-50 to-white">
<div class="text-base font-black text-cyan-900">Self-Consistency</div>
<div class="mt-1 text-[10px] font-semibold text-cyan-700">many reasoning paths &#8594; vote</div>
</div>
<div class="px-3 py-2.5 rounded-xl border-2 border-amber-200 bg-gradient-to-b from-amber-50 to-white">
<div class="text-base font-black text-amber-900">Tree of Thoughts</div>
<div class="mt-1 text-[10px] font-semibold text-amber-700">branch &#8594; evaluate &#8594; backtrack</div>
</div>
<div class="px-3 py-2.5 rounded-xl border-2 border-emerald-200 bg-gradient-to-b from-emerald-50 to-white">
<div class="text-base font-black text-emerald-900">ReAct</div>
<div class="mt-1 text-[10px] font-semibold text-emerald-700">reason &#8594; act &#8594; observe</div>
</div>
</div>

<div class="mt-4 rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
<div class="grid grid-cols-12 bg-slate-900 text-white text-[10px] font-bold uppercase tracking-[0.11em]">
<div class="col-span-2 px-3 py-2.5">Method</div>
<div class="col-span-3 px-3 py-2.5">Reasoning structure</div>
<div class="col-span-1 px-2 py-2.5 text-center">Compute</div>
<div class="col-span-3 px-3 py-2.5">Best suited for</div>
<div class="col-span-3 px-3 py-2.5">Main trade-off</div>
</div>

<div class="grid grid-cols-12 items-center bg-white border-b border-slate-100 text-[11px] leading-4">
<div class="col-span-2 px-3 py-3"><span class="px-2.5 py-1 rounded-full bg-blue-100 text-blue-800 font-bold">CoT</span></div>
<div class="col-span-3 px-3 py-3 font-semibold text-slate-700">One explicit reasoning path</div>
<div class="col-span-1 px-2 py-3 text-center"><span class="text-emerald-600 font-bold">Low</span></div>
<div class="col-span-3 px-3 py-3 text-slate-600">Multi-step decomposition</div>
<div class="col-span-3 px-3 py-3 text-slate-600">A plausible path can still be wrong</div>
</div>

<div class="grid grid-cols-12 items-center bg-cyan-50/40 border-b border-slate-100 text-[11px] leading-4">
<div class="col-span-2 px-3 py-3"><span class="px-2.5 py-1 rounded-full bg-cyan-100 text-cyan-800 font-bold">Self-Consistency</span></div>
<div class="col-span-3 px-3 py-3 font-semibold text-slate-700">Sample paths, aggregate answers</div>
<div class="col-span-1 px-2 py-3 text-center"><span class="text-amber-600 font-bold">Medium</span></div>
<div class="col-span-3 px-3 py-3 text-slate-600">Stable answer selection</div>
<div class="col-span-3 px-3 py-3 text-slate-600">Requires multiple rollouts</div>
</div>

<div class="grid grid-cols-12 items-center bg-white border-b border-slate-100 text-[11px] leading-4">
<div class="col-span-2 px-3 py-3"><span class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 font-bold">ToT</span></div>
<div class="col-span-3 px-3 py-3 font-semibold text-slate-700">Search a branching reasoning tree</div>
<div class="col-span-1 px-2 py-3 text-center"><span class="text-rose-600 font-bold">High</span></div>
<div class="col-span-3 px-3 py-3 text-slate-600">Planning and backtracking</div>
<div class="col-span-3 px-3 py-3 text-slate-600">Search-controller overhead</div>
</div>

<div class="grid grid-cols-12 items-center bg-emerald-50/40 text-[11px] leading-4">
<div class="col-span-2 px-3 py-3"><span class="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 font-bold">ReAct</span></div>
<div class="col-span-3 px-3 py-3 font-semibold text-slate-700">Reasoning grounded by observations</div>
<div class="col-span-1 px-2 py-3 text-center"><span class="text-sky-600 font-bold">Variable</span></div>
<div class="col-span-3 px-3 py-3 text-slate-600">Tool use and information gathering</div>
<div class="col-span-3 px-3 py-3 text-slate-600">Depends on tool reliability</div>
</div>
</div>

<div class="mt-3 px-4 py-2 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between text-[11px]">
<span>These methods allocate inference compute differently.</span>
<span class="font-bold text-slate-700">Model parameters remain fixed.</span>
</div>

---

# From Search to Training

<div class="grid grid-cols-2 gap-8 mt-6">

<div>

## Search-style reasoning

- Spend more compute at inference time.
- Try several paths, then select or vote.
- Works even when no training data are available.
- Cost grows with the number of sampled paths.

</div>

<div>

## RL-style reasoning

- Sample complete responses during training.
- Score each response with a verifier to obtain a reward.
- Move probability mass toward successful responses.
- Cost is paid during post-training, not every query.

</div>

</div>

<div class="mt-8 p-4 bg-gray-50 border-l-4 border-gray-500 text-lg">
The bridge is simple: if a final answer can be verified, the complete response becomes trainable.
</div>

---
routeAlias: rlvr
---

# RLVR: From Preference to Verification

<div class="flex justify-center mt-3">
<img src="/figs/demystify-rlvr-approaches.png" class="w-full max-h-[405px] object-contain" />
</div>

<div class="mt-3 p-3 rounded-xl border-l-4 border-red-500 bg-red-50 text-[15px] leading-6 text-center">
RLVR turns a reasoning task into an RL problem whenever the final answer can be checked automatically.
</div>

---

# RLVR: Verifiable Rewards

<div class="grid grid-cols-2 gap-5 mt-4">

<div class="p-4 rounded-2xl border-2 border-slate-200 bg-slate-50">
<div class="text-sm uppercase tracking-wide text-slate-500 font-bold mb-3">Preference-Based Feedback</div>
<div class="text-xl font-semibold mb-4">“Which response is better?”</div>
<div class="space-y-2 text-[15px] leading-6">
<div>Human preferences may be subjective.</div>
<div>A learned reward model may be inaccurate.</div>
<div>Correctness is only indirectly represented.</div>
</div>
</div>

<div class="p-4 rounded-2xl border-2 border-emerald-200 bg-emerald-50">
<div class="text-sm uppercase tracking-wide text-emerald-700 font-bold mb-3">Verifiable Feedback</div>
<div class="text-xl font-semibold mb-3">“Is this answer correct?”</div>
<MathTex display tex="r(x,y)=\begin{cases}1,&\text{verified correct},\\0,&\text{otherwise.}\end{cases}" class="text-[0.82em]" />
</div>

</div>

<div class="grid grid-cols-3 gap-4 mt-5 text-[14px] leading-5.5">
<div class="p-3 rounded-xl border border-blue-200 bg-blue-50"><b>Code</b><br>Run unit tests.</div>
<div class="p-3 rounded-xl border border-orange-200 bg-orange-50"><b>Mathematics</b><br>Check the final answer.</div>
<div class="p-3 rounded-xl border border-violet-200 bg-violet-50"><b>Logic</b><br>Verify constraints or a proof.</div>
</div>

<div class="mt-4 text-[14px] text-center font-semibold">
The reward is sparse, but objective, automatic, and scalable.
</div>

---

# RLVR: From REINFORCE to Reasoning

<div class="grid grid-cols-3 gap-4 mt-5 text-center">

<div class="p-4 rounded-2xl border-2 border-blue-200 bg-blue-50">
<div class="text-xs uppercase tracking-wide text-blue-700 font-bold mb-2">1. Prompt</div>
<MathTex display tex="x\sim\mathcal D" class="text-[0.95em]" />
<div class="text-[13px] leading-5 mt-2">sample a problem from the training distribution</div>
</div>

<div class="p-4 rounded-2xl border-2 border-rose-200 bg-rose-50">
<div class="text-xs uppercase tracking-wide text-rose-700 font-bold mb-2">2. Response</div>
<MathTex display tex="y\sim\pi_\theta(\cdot\mid x)" class="text-[0.95em]" />
<div class="text-[13px] leading-5 mt-2">generate the complete response: reasoning trace + final answer</div>
</div>

<div class="p-4 rounded-2xl border-2 border-emerald-200 bg-emerald-50">
<div class="text-xs uppercase tracking-wide text-emerald-700 font-bold mb-2">3. Verification</div>
<MathTex display tex="r=r(x,y)" class="text-[0.95em]" />
<div class="text-[13px] leading-5 mt-2">score the sampled response with a verifier</div>
</div>

</div>

<div class="mt-6 p-5 rounded-2xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-2">REINFORCE Update</div>
<MathTex display tex="\theta\leftarrow\theta+\eta\,\underbrace{\nabla_\theta\log\pi_\theta(y\mid x)}_{\text{policy score}}\,\underbrace{r}_{\text{verifiable reward}}" class="text-[0.94em]" />
</div>

<div class="mt-4 p-3 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[14px] leading-5.5">
A correct response receives a positive update; an incorrect response provides little or no positive signal.
</div>

---

# RLVR: Variance Reduction with a Baseline

<div class="mt-3 p-4 rounded-2xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-2">One Gradient Form, Different Baselines</div>
<MathTex display tex="\widehat g_b(\theta)=\nabla_\theta\log\pi_\theta(y\mid x)\,[r-b(x)],\qquad \mathbb E_{y\sim\pi_\theta(\cdot\mid x)}\!\left[b(x)\nabla_\theta\log\pi_\theta(y\mid x)\right]=0" class="text-[0.74em]" />
<div class="mt-2 text-[13px] leading-5">
A prompt-dependent baseline changes the variance of the gradient estimator, but not its expectation.
</div>
</div>

<div class="mt-4 grid grid-cols-3 gap-4 text-[12px] leading-5 items-stretch">

<div class="p-4 rounded-2xl border-2 border-slate-200 bg-slate-50 text-center">
<div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-2">No Baseline</div>
<div class="text-lg font-bold mb-2">Vanilla RLVR</div>
<MathTex display tex="b^{\mathrm{vanilla}}(x)=0" class="text-[0.88em]" />
<div class="mt-3 text-left">
Uses the raw verifier reward. It is simple and critic-free, but the policy-gradient estimate can have high variance.
</div>
</div>

<div class="p-4 rounded-2xl border-2 border-blue-200 bg-blue-50 text-center">
<div class="text-xs uppercase tracking-wide text-blue-700 font-bold mb-2">Learned Baseline</div>
<div class="text-lg font-bold text-blue-900 mb-2">PPO <span class="text-[10px] font-normal text-blue-600">(Schulman et al., 2017)</span></div>
<MathTex display tex="b^{\mathrm{PPO}}_\phi(x)=\widehat V_\phi(x)\approx V^{\pi_\theta}(x)" class="text-[0.76em]" />
<div class="mt-3 text-left">
Trains a separate critic to approximate the value function, reducing variance at the cost of extra memory and optimization.
</div>
</div>

<div class="p-4 rounded-2xl border-2 border-orange-200 bg-orange-50 text-center">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-2">Ideal Baseline</div>
<div class="text-lg font-bold text-orange-900 mb-2">Oracle</div>
<MathTex display tex="b^{\mathrm{oracle}}(x)=V^{\pi_\theta}(x)=\mathbb E[r\mid x]" class="text-[0.76em]" />
<div class="mt-3 text-left">
Uses the true expected reward for each prompt. It is the statistical target, but it is unknown during training.
</div>
</div>

</div>

<div class="mt-4 p-3 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[13px] leading-5 text-center font-semibold">
PPO learns a critic to approach the oracle; GRPO instead approximates it with rewards from multiple responses.
</div>

---

# RLVR: Minibatch Policy Gradient

<div class="flex justify-center mt-2">
<img src="/figs/demystify-minibatch-xyr.png" class="w-full max-h-[365px] object-contain" />
</div>

<div class="mt-3 p-3 rounded-xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-[10px] uppercase tracking-wide text-violet-700 font-bold mb-1">Minibatch Gradient Estimator</div>
<MathTex display tex="\widehat g_b(\theta)=\frac{1}{B}\sum_{b=1}^{B}\nabla_\theta\log\pi_\theta(y_b\mid x_b)\,[r_b-b(x_b)]" class="text-[0.74em]" />
</div>

---

# RLVR: The Oracle Baseline

<div class="flex justify-center mt-2">
<img src="/figs/demystify-oracle-xyr.png" class="w-full max-h-[350px] object-contain" />
</div>

<div class="grid grid-cols-2 gap-5 mt-3 text-[13px] leading-5.5">
<div class="p-3 rounded-xl border-2 border-emerald-200 bg-emerald-50 text-center">
<div class="text-xs uppercase tracking-wide text-emerald-700 font-bold mb-1">Oracle Advantage</div>
<MathTex display tex="A^{\mathrm{oracle}}(x,y)=r(x,y)-V^{\pi_\theta}(x)" class="text-[0.80em]" />
</div>
<div class="p-3 rounded-xl border-2 border-orange-200 bg-orange-50">
The value function is unknown and usually requires a separate critic. Estimating that critic adds memory, computation, and estimation error.
</div>
</div>

---

# GRPO: Group Statistics Replace the Critic

<div class="relative flex justify-center mt-2">
<img src="/figs/demystify-grpo-idea.png" class="w-full max-h-[400px] object-contain" />
<div class="absolute left-[53%] top-[76%] w-[43%] h-[16%] bg-white flex items-center justify-center">
<MathTex display tex="\mathrm{Advantage}_i=r_i-\mathrm{mean}(r)" class="text-[0.78em]" />
</div>
</div>

<div class="mt-3 p-3 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[14px] leading-5.5 text-center">
For each prompt, sample multiple responses and replace the unknown value baseline with the group mean reward.
</div>

---

# GRPO-type Algorithm

<div class="flex justify-center mt-2">
<img src="/figs/demystify-grpo-type-xyr.png" class="w-full max-h-[390px] object-contain" />
</div>

---

# GRPO: Objective

<div class="text-xs px-3 py-1.5 rounded bg-violet-50 border border-violet-200 inline-block">
Group-relative surrogate objective.
</div>

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta)
=
\mathbb{E}_{x\sim\mathcal D,\,\{y_i\}_{i=1}^{G}\overset{\mathrm{i.i.d.}}{\sim}\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)}
\left[
\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|y_i|}
\sum_{t=1}^{|y_i|}
\rho_{i,t}
\hat A_{i,t}
\right]
$$

$$
\rho_{i,t}
=
\frac{\pi_\theta(y_{i,t}\mid x,y_{i,<t})}
{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid x,y_{i,<t})},
\qquad
\hat A_{i,t}
=
\hat A_i
=
\frac{r_i-\mathrm{mean}(r_1,\ldots,r_G)}
{\mathrm{std}(r_1,\ldots,r_G)+\epsilon}.
$$

<div class="grid grid-cols-3 gap-3 mt-5 text-[12px] leading-4.8">
<div class="p-3 rounded-xl border-2 border-slate-200 bg-white">
<div class="font-bold mb-1 text-slate-700"><MathTex tex="x,\ y_i,\ r_i" /></div>
Prompt <MathTex tex="x" />, sampled response <MathTex tex="y_i" />, and reward <MathTex tex="r_i=r(x,y_i)" />.
</div>
<div class="p-3 rounded-xl border-2 border-emerald-200 bg-emerald-50">
<div class="font-bold mb-1 text-emerald-800"><MathTex tex="\hat A_{i,t}" /></div>
Reward <MathTex tex="r_i" /> normalized inside the group.
</div>
<div class="p-3 rounded-xl border-2 border-orange-200 bg-orange-50">
<div class="font-bold mb-1 text-orange-800"><MathTex tex="\rho_{i,t}" /></div>
Current-policy probability divided by rollout-policy probability.
</div>
</div>

<div class="mt-3 p-2.5 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[14px] leading-5.5">
GRPO = <b>group sampling</b> + <b>relative advantage</b> + <b>importance weighting</b> + <b>length normalization</b>.
</div>

---

# GRPO: Policy Gradient

<div class="text-xs px-3 py-1.5 rounded bg-violet-50 border border-violet-200 inline-block">
Corresponding policy-gradient form.
</div>

$$
\nabla_\theta \mathcal{J}_{\mathrm{GRPO}}(\theta)
=
\mathbb{E}_{x\sim\mathcal D,\,\{y_i\}_{i=1}^{G}\overset{\mathrm{i.i.d.}}{\sim}\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)}
\Bigg[
\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|y_i|}
\sum_{t=1}^{|y_i|}
\rho_{i,t}\hat A_{i,t}\,s_{i,t}
\Bigg]
$$

$$
\begin{aligned}
\rho_{i,t}
&=
\frac{\pi_\theta(y_{i,t}\mid x,y_{i,<t})}
{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid x,y_{i,<t})}
&&\text{importance ratio},\\[4pt]
s_{i,t}
&:=
\nabla_\theta \log \pi_\theta(y_{i,t}\mid x,y_{i,<t})
&&\text{token-level score function}.
\end{aligned}
$$

<div class="mt-5 p-3 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[15px] leading-6">
Each token contributes <MathTex tex="\rho_{i,t}\hat A_{i,t}s_{i,t}" />: <b>importance ratio</b> × <b>group-relative coefficient</b> × <b>score function</b>.
</div>

---

# Example: Multiple Rollouts

<div class="mt-3 p-3 rounded-2xl border-2 border-slate-200 bg-slate-50 flex items-center justify-between">
<div>
<div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-1">One Prompt <MathTex tex="x" /></div>
<div class="text-[16px] leading-6">Find the shortest distance from <b>(5,5)</b> to the curve <b>uv = 4</b>.</div>
</div>
<div class="text-[12px] px-3 py-1.5 rounded-full bg-white border border-slate-200">four independent rollouts</div>
</div>

<div class="grid grid-cols-4 gap-3 mt-4 text-center">

<div class="p-3 rounded-2xl border-2 border-emerald-300 bg-emerald-50 min-h-[225px]">
<div class="flex items-center justify-between text-xs"><b class="text-emerald-800"><MathTex tex="y_1" /></b><span class="px-2 py-1 rounded-full bg-emerald-200 text-emerald-800">reward +1</span></div>
<div class="mt-5 text-[12px] leading-5 text-left">Lagrange multipliers give the closest point <b>(4,1)</b>.</div>
<div class="mt-5 text-xs uppercase tracking-wide text-emerald-700 font-bold">Final Answer</div>
<div class="mt-1 text-3xl font-bold text-emerald-800">√17</div>
</div>

<div class="p-3 rounded-2xl border-2 border-rose-200 bg-rose-50 min-h-[225px]">
<div class="flex items-center justify-between text-xs"><b class="text-rose-800"><MathTex tex="y_2" /></b><span class="px-2 py-1 rounded-full bg-rose-200 text-rose-800">reward -1</span></div>
<div class="mt-5 text-[12px] leading-5 text-left">Assumes symmetry and chooses the point <b>(2,2)</b>.</div>
<div class="mt-5 text-xs uppercase tracking-wide text-rose-700 font-bold">Final Answer</div>
<div class="mt-1 text-3xl font-bold text-rose-800">√18</div>
</div>

<div class="p-3 rounded-2xl border-2 border-rose-200 bg-rose-50 min-h-[225px]">
<div class="flex items-center justify-between text-xs"><b class="text-rose-800"><MathTex tex="y_3" /></b><span class="px-2 py-1 rounded-full bg-rose-200 text-rose-800">reward -1</span></div>
<div class="mt-5 text-[12px] leading-5 text-left">Finds <b>(1,4)</b>, then miscomputes the Euclidean distance.</div>
<div class="mt-5 text-xs uppercase tracking-wide text-rose-700 font-bold">Final Answer</div>
<div class="mt-1 text-3xl font-bold text-rose-800">5</div>
</div>

<div class="p-3 rounded-2xl border-2 border-rose-200 bg-rose-50 min-h-[225px]">
<div class="flex items-center justify-between text-xs"><b class="text-rose-800"><MathTex tex="y_4" /></b><span class="px-2 py-1 rounded-full bg-rose-200 text-rose-800">reward -1</span></div>
<div class="mt-5 text-[12px] leading-5 text-left">Projects toward the diagonal without solving the constraint.</div>
<div class="mt-5 text-xs uppercase tracking-wide text-rose-700 font-bold">Final Answer</div>
<div class="mt-1 text-3xl font-bold text-rose-800">3</div>
</div>

</div>

<div class="mt-4 p-3 rounded-xl border-l-4 border-violet-500 bg-violet-50 text-[14px] leading-5 text-center">
The verifier converts the rollout group into <MathTex tex="[r_1,r_2,r_3,r_4]=[1,-1,-1,-1]" />.
</div>

---
clicks: 4
---

# Example: Reward Normalization

<div class="mt-2 grid grid-cols-3 gap-4 items-stretch">

<div class="p-3 rounded-2xl border-2 border-slate-200 bg-white text-center">
<div class="text-xs uppercase tracking-wide text-slate-500 font-bold mb-2">Verifier Rewards</div>
<div class="flex justify-center gap-2 text-sm font-bold">
<div class="px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800">+1</div>
<div class="px-3 py-1.5 rounded-lg bg-rose-100 text-rose-800">-1</div>
<div class="px-3 py-1.5 rounded-lg bg-rose-100 text-rose-800">-1</div>
<div class="px-3 py-1.5 rounded-lg bg-rose-100 text-rose-800">-1</div>
</div>
<MathTex display tex="\mathbf r=[1,-1,-1,-1]" class="text-[0.74em] mt-2" />
</div>

<div v-click="1" class="p-3 rounded-2xl border-2 border-blue-200 bg-blue-50 text-center">
<div class="text-xs uppercase tracking-wide text-blue-700 font-bold mb-1">Group Statistics</div>
<MathTex display tex="\bar r=\frac14\sum_{j=1}^4r_j=-0.5" class="text-[0.69em]" />
<MathTex display tex="\sigma_r=\sqrt{\frac14\sum_{j=1}^4(r_j-\bar r)^2}\approx0.866" class="text-[0.61em] mt-1" />
</div>

<div v-click="2" class="p-3 rounded-2xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-1">Normalized Advantages</div>
<MathTex display tex="\hat A_i=\frac{r_i-\bar r}{\sigma_r}" class="text-[0.74em]" />
<MathTex display tex="\widehat{\mathbf A}=[1.73,-0.58,-0.58,-0.58]" class="text-[0.64em] mt-1" />
</div>

</div>

<div v-click="3" class="mt-3 px-4 py-2 rounded-xl border border-sky-200 bg-sky-50 grid grid-cols-[190px_1fr] items-center gap-4">
<div class="text-[10px] uppercase tracking-wide text-sky-700 font-bold">Autoregressive Policy Score</div>
<MathTex display tex="\pi_\theta(y_i\mid x)=\prod_{t=1}^{|y_i|}\pi_\theta(y_{i,t}\mid x,y_{i,<t}),\qquad s_i=\nabla_\theta\log\pi_\theta(y_i\mid x)=\sum_{t=1}^{|y_i|}s_{i,t}" class="text-[0.60em]" />
</div>

<div v-click="4" class="mt-3 p-3 rounded-2xl border-2 border-emerald-200 bg-emerald-50">
<div class="flex items-center justify-between mb-2">
<div class="text-xs uppercase tracking-wide text-emerald-700 font-bold">One Sequence Advantage Multiplies Every Token Score</div>
<div class="text-[11px] text-emerald-800/70"><MathTex tex="\hat A_{i,t}=\hat A_i" /></div>
</div>

<div class="grid grid-cols-4 gap-3 text-center text-[10px]">
<div><div class="font-bold text-emerald-800 mb-1"><MathTex tex="\hat A_1=1.73" /></div><div class="flex justify-center items-center gap-1"><span class="px-1.5 py-1 rounded bg-emerald-200"><MathTex tex="y_{1,1}" /><br><b>+1.73</b></span><span class="px-1.5 py-1 rounded bg-emerald-200"><MathTex tex="y_{1,2}" /><br><b>+1.73</b></span><span>…</span><span class="px-1.5 py-1 rounded bg-emerald-200"><MathTex tex="y_{1,|y_1|}" /><br><b>+1.73</b></span></div></div>
<div><div class="font-bold text-rose-800 mb-1"><MathTex tex="\hat A_2=-0.58" /></div><div class="flex justify-center items-center gap-1"><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{2,1}" /><br><b>-0.58</b></span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{2,2}" /><br><b>-0.58</b></span><span>…</span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{2,|y_2|}" /><br><b>-0.58</b></span></div></div>
<div><div class="font-bold text-rose-800 mb-1"><MathTex tex="\hat A_3=-0.58" /></div><div class="flex justify-center items-center gap-1"><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{3,1}" /><br><b>-0.58</b></span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{3,2}" /><br><b>-0.58</b></span><span>…</span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{3,|y_3|}" /><br><b>-0.58</b></span></div></div>
<div><div class="font-bold text-rose-800 mb-1"><MathTex tex="\hat A_4=-0.58" /></div><div class="flex justify-center items-center gap-1"><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{4,1}" /><br><b>-0.58</b></span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{4,2}" /><br><b>-0.58</b></span><span>…</span><span class="px-1.5 py-1 rounded bg-rose-200"><MathTex tex="y_{4,|y_4|}" /><br><b>-0.58</b></span></div></div>
</div>
</div>

<div class="mt-3 p-2 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-center">
Centering compares rollouts within a prompt; the same sequence-level coefficient is paired with each token-specific score <MathTex tex="s_{i,t}" />.
</div>

---
clicks: 2
---

# Example: Importance Ratio

<div class="grid grid-cols-5 gap-3 mt-3 text-[12px] leading-5">
<div class="col-span-2 p-3 rounded-xl border-2 border-slate-200 bg-slate-50">
<div class="text-[10px] uppercase tracking-wide text-slate-500 font-bold mb-1">Prompt <MathTex tex="x" /></div>
<div class="font-mono bg-white px-2 py-1 rounded">Find the shortest distance.</div>
</div>
<div class="col-span-2 p-3 rounded-xl border-2 border-slate-200 bg-slate-50">
<div class="text-[10px] uppercase tracking-wide text-slate-500 font-bold mb-1">Prefix <MathTex tex="y_{1,<t}" /></div>
<div class="font-mono bg-white px-2 py-1 rounded">The shortest distance is _____</div>
</div>
<div class="p-3 rounded-xl border-2 border-emerald-200 bg-emerald-50 text-center">
<div class="text-[10px] uppercase tracking-wide text-emerald-700 font-bold mb-1">Token <MathTex tex="y_{1,t}" /></div>
<div class="font-mono text-xl font-bold text-emerald-800">√17</div>
</div>
</div>

<div v-click="1" class="grid grid-cols-2 gap-4 mt-4">

<div class="p-3 rounded-2xl border-2 border-sky-200 bg-sky-50">
<div class="font-bold text-sky-800 mb-2 text-[13px]">Rollout policy <MathTex tex="\pi_{\theta_{\mathrm{old}}}" /></div>
<div class="space-y-2 text-[12px]">
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-mono font-bold text-center">√17</div><div class="flex-1 h-3 rounded-full bg-sky-100 overflow-hidden"><div class="h-full bg-sky-500" style="width:20%"></div></div><div class="w-10 text-right">0.20</div></div>
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-center">√18</div><div class="flex-1 h-3 rounded-full bg-sky-100 overflow-hidden"><div class="h-full bg-sky-400" style="width:45%"></div></div><div class="w-10 text-right">0.45</div></div>
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-center">3</div><div class="flex-1 h-3 rounded-full bg-sky-100 overflow-hidden"><div class="h-full bg-sky-400" style="width:35%"></div></div><div class="w-10 text-right">0.35</div></div>
</div>
</div>

<div class="p-3 rounded-2xl border-2 border-emerald-200 bg-emerald-50">
<div class="font-bold text-emerald-800 mb-2 text-[13px]">Current policy <MathTex tex="\pi_\theta" /></div>
<div class="space-y-2 text-[12px]">
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-mono font-bold text-center">√17</div><div class="flex-1 h-3 rounded-full bg-emerald-100 overflow-hidden"><div class="h-full bg-emerald-500" style="width:30%"></div></div><div class="w-10 text-right">0.30</div></div>
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-center">√18</div><div class="flex-1 h-3 rounded-full bg-emerald-100 overflow-hidden"><div class="h-full bg-emerald-400" style="width:35%"></div></div><div class="w-10 text-right">0.35</div></div>
<div class="flex items-center gap-2"><div class="w-13 px-2 py-0.5 rounded bg-white border border-slate-200 font-mono text-center">3</div><div class="flex-1 h-3 rounded-full bg-emerald-100 overflow-hidden"><div class="h-full bg-emerald-400" style="width:35%"></div></div><div class="w-10 text-right">0.35</div></div>
</div>
</div>

</div>

<div v-click="2" class="grid grid-cols-5 gap-4 mt-4 items-stretch">
<div class="col-span-3 p-3 rounded-2xl border-2 border-orange-300 bg-orange-50 text-center">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-1">Sampled-Token Importance Ratio</div>
<MathTex display tex="\rho_{1,t}=\frac{\pi_\theta(\sqrt{17}\mid x,y_{1,<t})}{\pi_{\theta_{\mathrm{old}}}(\sqrt{17}\mid x,y_{1,<t})}=\frac{0.30}{0.20}=1.5" class="text-[0.78em]" />
</div>
<div class="col-span-2 p-3 rounded-2xl border-2 border-amber-200 bg-amber-50 text-[12px] leading-5.5">
Samples come from <MathTex tex="\pi_{\theta_{\mathrm{old}}}" />, while optimization targets <MathTex tex="\pi_\theta" />. The ratio reweights the sampled token for the current policy: <b><MathTex tex="\rho>1" /> upweights</b>, <b><MathTex tex="\rho<1" /> downweights</b>.
</div>
</div>

---
clicks: 2
---

# Example: Full Update

<div class="grid grid-cols-3 gap-3 mt-2 text-center text-[12px]">
<div class="p-3 rounded-xl border-2 border-slate-200 bg-white"><div class="text-[10px] uppercase tracking-wide text-slate-500 font-bold mb-1">Rollout Group</div><MathTex tex="\{y_j\}_{j=1}^4\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)" /></div>
<div class="p-3 rounded-xl border-2 border-blue-200 bg-blue-50"><div class="text-[10px] uppercase tracking-wide text-blue-700 font-bold mb-1">Verifier Rewards</div><MathTex tex="\mathbf r=[1,-1,-1,-1]" /></div>
<div class="p-3 rounded-xl border-2 border-violet-200 bg-violet-50"><div class="text-[10px] uppercase tracking-wide text-violet-700 font-bold mb-1">Relative Advantages</div><MathTex tex="\widehat{\mathbf A}=[1.73,-0.58,-0.58,-0.58]" /></div>
</div>

<div class="mt-3 p-2.5 rounded-xl border-l-4 border-emerald-500 bg-emerald-50 text-[12px] text-center">
For the correct response <MathTex tex="y_1" />, every token uses the sequence coefficient <MathTex tex="\hat A_1=1.73" />.
</div>

<div v-click="1" class="grid grid-cols-3 gap-3 mt-3 text-center">
<div class="p-2.5 rounded-xl border-2 border-orange-200 bg-orange-50"><div class="text-xs font-bold text-orange-800 mb-1">Token 1</div><div class="flex justify-center gap-4 text-[11px]"><span>ratio <MathTex tex="\rho_{1,1}=1.5" /></span><span>score <MathTex tex="s_{1,1}" /></span></div></div>
<div class="p-2.5 rounded-xl border-2 border-orange-200 bg-orange-50"><div class="text-xs font-bold text-orange-800 mb-1">Token 2</div><div class="flex justify-center gap-4 text-[11px]"><span>ratio <MathTex tex="\rho_{1,2}=0.8" /></span><span>score <MathTex tex="s_{1,2}" /></span></div></div>
<div class="p-2.5 rounded-xl border-2 border-orange-200 bg-orange-50"><div class="text-xs font-bold text-orange-800 mb-1">Token 3</div><div class="flex justify-center gap-4 text-[11px]"><span>ratio <MathTex tex="\rho_{1,3}=1.2" /></span><span>score <MathTex tex="s_{1,3}" /></span></div></div>
</div>

<div v-click="2" class="grid grid-cols-5 gap-4 mt-3">
<div class="col-span-3 p-3 rounded-2xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-1">Policy Gradient Contribution</div>
<MathTex display tex="g_1(\theta)=\frac{1}{3}\sum_{t=1}^{3}\rho_{1,t}\hat A_1s_{1,t}" class="text-[0.82em]" />
<MathTex display tex="g_1(\theta)=\frac{1}{3}\left(1.5\times1.73\,s_{1,1}+0.8\times1.73\,s_{1,2}+1.2\times1.73\,s_{1,3}\right)" class="text-[0.76em] mt-1" />
</div>
<div class="col-span-2 p-3 rounded-2xl border-2 border-sky-200 bg-sky-50 text-center">
<div class="text-xs uppercase tracking-wide text-sky-700 font-bold mb-1">Objective and Loss</div>
<MathTex display tex="J_1(\theta)=\frac13\sum_{t=1}^{3}\rho_{1,t}\hat A_1,\qquad L_1(\theta)=-J_1(\theta)" class="text-[0.74em]" />
<MathTex display tex="\nabla_\theta J_1(\theta)=g_1(\theta),\qquad \nabla_\theta L_1(\theta)=-g_1(\theta)" class="text-[0.69em] mt-2" />
</div>
</div>

---

# Dr. GRPO: Removing Optimization Bias

<div class="grid grid-cols-5 gap-5 mt-3 h-[420px] items-stretch">

<div class="col-span-3 p-3 rounded-2xl border-2 border-slate-200 bg-white shadow-sm flex items-center justify-center">
<img src="/figs/drgrpo-xyr.png" class="w-full max-h-[410px] object-contain" />
</div>

<div class="col-span-2 flex flex-col gap-3">

<div class="p-3 rounded-2xl border-2 border-rose-200 bg-rose-50">
<div class="text-xs uppercase tracking-wide text-rose-700 font-bold mb-2">Two Sources of Bias in GRPO</div>
<div class="space-y-1.5 text-[12px] leading-5">
<div><b>Response length:</b> averaging each response loss by <MathTex tex="|y_i|" /> changes its effective weight.</div>
<div><b>Prompt difficulty:</b> dividing centered rewards by their group standard deviation reweights prompts.</div>
</div>
</div>

<div class="flex-1 p-3 rounded-2xl border-2 border-emerald-200 bg-emerald-50">
<div class="text-xs uppercase tracking-wide text-emerald-700 font-bold mb-2">Dr. GRPO</div>
<MathTex display tex="\widehat b_i^{\mathrm{Dr}}=\frac1G\sum_{j=1}^{G}r_j,\qquad \widehat A_i^{\mathrm{Dr}}=r_i-\widehat b_i^{\mathrm{Dr}}" class="text-[0.76em]" />
<div class="mt-2 text-[12px] leading-5">
Keep group centering, but remove response-length and reward-standard-deviation normalization.
</div>
<div class="mt-3 px-3 py-2.5 rounded-xl border-l-4 border-emerald-500 bg-white/80 text-[12px] leading-5 font-semibold">
Together, these two changes recover the standard policy-gradient form without bias.
</div>
</div>

</div>
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin. "Understanding R1-Zero-Like Training: A Critical Perspective." arXiv preprint arXiv:2503.20783 (2025).
</div>

---

# GPG: Group Policy Gradient

<div class="mt-2 text-[14px] leading-5.5 text-slate-700">
GPG returns to a direct group-centered policy-gradient loss, using the group mean reward as a critic-free baseline.
</div>

<div class="mt-3 py-3 border-y border-slate-300">
<MathTex display tex="\mathcal L_{\mathrm{GPG}}(\theta)=-\mathbb E_{x,\{y_i\}_{i=1}^{G}}\!\left[\frac{1}{\sum_{i=1}^{G}|y_i|}\sum_{i=1}^{G}\sum_{t=1}^{|y_i|}\log\pi_\theta(y_{i,t}\mid x,y_{i,<t})\,\hat A_i\right]" class="text-[0.67em]" />
</div>

<div class="grid grid-cols-2 gap-8 mt-4 text-[13px] leading-5.5">

<div>
<div class="text-xs uppercase tracking-wide text-blue-700 font-bold mb-2">Group Reward</div>
<MathTex display tex="\bar r=\frac1G\sum_{j=1}^{G}r_j,\qquad \hat A_i=\frac{r_i-\bar r}{F_{\mathrm{norm}}}" class="text-[0.78em]" />
<div class="mt-3">
The loss is normalized by the <b>total number of generated tokens</b>, rather than normalizing each response separately. <MathTex tex="F_{\mathrm{norm}}" /> is optional.
</div>
</div>

<div class="border-l border-slate-300 pl-8">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-2">Accurate Gradient Estimation (AGE)</div>
<MathTex display tex="\widehat g_{\mathrm{AGE}}=\alpha\widehat g,\qquad \alpha=\frac{B}{B-M}" class="text-[0.82em]" />
<div class="mt-3">
If <MathTex tex="M" /> of the <MathTex tex="B" /> sampled groups are all correct or all wrong, group centering makes their gradients zero. AGE averages over the remaining <MathTex tex="B-M" /> informative groups.
</div>
</div>

</div>

<div class="mt-4 px-4 py-3 rounded-xl border-l-4 border-emerald-500 bg-emerald-50 text-[13px] leading-5.5 text-center font-semibold">
Minimal design: no critic, no reference model, no KL penalty, and no importance sampling.
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Xiangxiang Chu, Hailang Huang, Xiao Zhang, Fei Wei, and Yong Wang. "GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning." arXiv preprint arXiv:2504.02546 (2025).
</div>

---

# Demystify GRPO: A Second-Order U-Statistic

<div class="mt-2 p-3 rounded-xl border border-slate-200 bg-slate-50 text-[13px] leading-5.5">
For the on-policy GRPO-type gradient with a group-mean baseline, fix one prompt <MathTex tex="x" /> and draw a group of responses. For each response, let <MathTex tex="r_i=r(x,y_i)" />; its response-level score aggregates the token scores:
<MathTex display tex="y_1,\ldots,y_G\overset{\mathrm{i.i.d.}}{\sim}\pi_\theta(\cdot\mid x),\qquad s_i(\theta):=\nabla_\theta\log\pi_\theta(y_i\mid x)=\sum_{t=1}^{|y_i|}s_{i,t},\qquad \bar r=\frac{1}{G}\sum_{i=1}^{G}r_i." class="text-[0.70em] mt-1" />
</div>

<div class="grid grid-cols-2 gap-4 mt-4 items-stretch">

<div class="p-4 rounded-2xl border-2 border-violet-200 bg-violet-50 text-center">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-2">Centered-Reward Form</div>
<MathTex display tex="\widehat g_{\mathrm{GRPO}}(x;\theta)=\frac{1}{G-1}\sum_{i=1}^{G}s_i(\theta)(r_i-\bar r)" class="text-[0.80em]" />
<div class="mt-3 text-[13px] leading-5 text-left">
Each score is multiplied by its reward relative to the other responses for the same prompt.
</div>
</div>

<div class="p-4 rounded-2xl border-2 border-orange-200 bg-orange-50 text-center">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-2">Equivalent Pairwise Form</div>
<MathTex display tex="\widehat g_{\mathrm{GRPO}}(x;\theta)=\binom{G}{2}^{-1}\sum_{1\le i<j\le G}\frac{1}{2}(s_i-s_j)(r_i-r_j)" class="text-[0.72em]" />
<div class="mt-3 text-[13px] leading-5 text-left">
The group-centered gradient is an average over every unordered pair of sampled responses.
</div>
</div>

</div>

<div class="mt-4 p-3 rounded-xl border-l-4 border-emerald-500 bg-emerald-50 text-[14px] leading-5.5 text-center">
With kernel <MathTex tex="h((y_i,r_i),(y_j,r_j)):=\tfrac12(s_i-s_j)(r_i-r_j)" />, this is exactly a second-order U-statistic in the sampled response-reward pairs.
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Hongyi Zhou, Kai Ye, Erhan Xu, Jin Zhu, Ying Yang, Shijin Gong, and Chengchun Shi. "Demystifying Group Relative Policy Optimization: Its Policy Gradient is a U-Statistic." arXiv preprint arXiv:2603.01162 (2026).
</div>

---

# Demystify GRPO: Theoretical Results

<div class="flex justify-center items-center mt-7">
<img src="/figs/demystify-theory-roadmap.png" class="w-full max-h-[430px] object-contain" />
</div>

<div class="mt-5 p-3 rounded-xl border-l-4 border-slate-500 bg-slate-50 text-[13px] leading-5 text-center">
The U-statistic representation connects gradient evaluation, policy optimization, and practical GRPO variants in one theoretical framework.
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Hongyi Zhou, Kai Ye, Erhan Xu, Jin Zhu, Ying Yang, Shijin Gong, and Chengchun Shi. "Demystifying Group Relative Policy Optimization: Its Policy Gradient is a U-Statistic." arXiv preprint arXiv:2603.01162 (2026).
</div>

---

# KAE: Kernelized Advantage Estimation

<div class="flex justify-center mt-2">
<img src="/figs/kae-overview.png" class="w-full max-h-[235px] object-contain" />
</div>

<div class="mt-2 p-3 rounded-2xl border-2 border-orange-300 bg-orange-50/60">
<div class="grid grid-cols-5 gap-4 items-center">

<div class="col-span-3 text-center">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-1">Kernel Baseline Across Training Time</div>
<MathTex display tex="\kappa_{t,s}=K\!\left(\frac{t-s}{th}\right),\qquad \widehat b_{i,t}^{\mathrm{KAE}}=\frac{\sum_{s<t}\kappa_{t,s}r_{i,s}}{\sum_{s<t}\kappa_{t,s}}" class="text-[0.72em]" />
</div>

<div class="col-span-2 text-center border-l-2 border-orange-200 pl-4">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-1">Advantage</div>
<MathTex display tex="\widehat A_{i,t}^{\mathrm{KAE}}=r_{i,t}-\widehat b_{i,t}^{\mathrm{KAE}}" class="text-[0.84em]" />
</div>

</div>
</div>

<div class="mt-2 p-2 rounded-lg bg-slate-50 border border-slate-200 text-[12px] leading-5 text-center">
For prompt <MathTex tex="x_i" />, iteration <MathTex tex="t" /> samples <MathTex tex="y_{i,t}\sim\pi_{\theta_t}(\cdot\mid x_i)" /> and observes <MathTex tex="r_{i,t}=r(x_i,y_{i,t})" />. The kernel input <MathTex tex="(t-s)/(th)" /> makes nearby iterations more influential when estimating the current baseline.
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Shijin Gong, Kai Ye, Jin Zhu, Xinyu Zhang, Hongyi Zhou, and Chengchun Shi. "Kernelized Advantage Estimation: From Nonparametric Statistics to LLM Reasoning." arXiv preprint arXiv:2604.28005 (2026).
</div>

---

# BASIS: Single-Rollout Information Sharing

<div class="mt-3 p-3 rounded-2xl border-2 border-orange-200 bg-white shadow-sm">
<img src="/figs/basis-pipeline.png" class="w-full max-h-[195px] object-contain" />
</div>

<div class="grid grid-cols-5 gap-4 mt-3 items-stretch">

<div class="col-span-3 p-3 rounded-2xl border-2 border-orange-300 bg-orange-50/60 text-center">
<div class="text-xs uppercase tracking-wide text-orange-700 font-bold mb-1">Batchwise Leave-One-Out Baseline</div>
<MathTex display tex="\widehat b_{i,t}^{\mathrm{BASIS}}=\sum_{j\ne i}w_{ij,t}r_{j,t},\qquad \widehat A_{i,t}^{\mathrm{BASIS}}=r_{i,t}-\widehat b_{i,t}^{\mathrm{BASIS}},\qquad w_{ii,t}=0" class="text-[0.70em]" />
<MathTex display tex="w_{ij,t}=\frac{\widehat V_{i,t}\widehat V_{j,t}/\widehat\sigma_{j,t}^{,2}}{\sum_{k\ne i}\widehat V_{k,t}^{,2}/\widehat\sigma_{k,t}^{,2}}" class="text-[0.76em] mt-1" />
</div>

<div class="col-span-2 p-3 rounded-2xl border-2 border-violet-200 bg-violet-50">
<div class="text-xs uppercase tracking-wide text-violet-700 font-bold mb-2">Core Idea</div>
<div class="text-[13px] leading-5.5">
For each prompt <MathTex tex="x_i" />, sample one response <MathTex tex="y_{i,t}\sim\pi_{\theta_t}(\cdot\mid x_i)" /> and obtain <MathTex tex="r_{i,t}=r(x_i,y_{i,t})" />. Estimate its baseline by sharing reward information across the batch.
</div>
</div>

</div>

<div class="mt-3 flex justify-center gap-3 text-[12px] font-semibold">
<div class="px-3 py-1.5 rounded-full bg-blue-50 border border-blue-200">one rollout: <MathTex tex="G=1" /></div>
<div class="px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200">prompt-dependent baseline</div>
<div class="px-3 py-1.5 rounded-full bg-orange-50 border border-orange-200">critic-free</div>
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Shijin Gong, Erhan Xu, Kai Ye, Francesco Quinzan, Giulia Livieri, and Chengchun Shi. "BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning." arXiv preprint arXiv:2605.27293 (2026).
</div>


---

# Over One Hundred XPO

<div class="grid grid-cols-9 gap-3 mt-3 items-center text-center">
<div class="col-span-4 px-4 py-2 rounded-xl border-2 border-slate-300 bg-slate-50"><b>PPO</b> <span class="text-[11px] text-slate-500">(Schulman et al., 2017)</span></div>
<div class="col-span-1 text-2xl text-slate-400">&#8594;</div>
<div class="col-span-4 px-4 py-2 rounded-xl border-2 border-violet-300 bg-violet-50"><b>GRPO / DeepSeekMath</b> <span class="text-[11px] text-violet-600">(Shao et al., 2024)</span></div>
</div>

<div class="grid grid-cols-5 gap-4 mt-3 items-stretch">

<div class="col-span-3 rounded-2xl border-2 border-blue-200 bg-blue-50/40 p-3">
<div class="mb-2 text-center text-[13px] font-bold uppercase tracking-wide text-blue-800">Algorithms & Empirical Work</div>
<div class="grid grid-cols-3 gap-1 text-center">
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">RLOO</b><span class="text-[8px] text-slate-500">(Ahmadian et al., 2024)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">REINFORCE++</b><span class="text-[8px] text-slate-500">(Hu et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">Dr. GRPO</b><span class="text-[8px] text-slate-500">(Liu et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">DAPO</b><span class="text-[8px] text-slate-500">(Yu et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">GPG</b><span class="text-[8px] text-slate-500">(Chu et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">GSPO</b><span class="text-[8px] text-slate-500">(Zheng et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">CPPO</b><span class="text-[8px] text-slate-500">(Lin et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">BNPO</b><span class="text-[8px] text-slate-500">(Xiao et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">SEED-GRPO</b><span class="text-[8px] text-slate-500">(Chen et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">GMPO</b><span class="text-[8px] text-slate-500">(Zhao et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">KRPO</b><span class="text-[8px] text-slate-500">(Wang et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">RePO</b><span class="text-[8px] text-slate-500">(Li et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">Single-Stream PO</b><span class="text-[8px] text-slate-500">(Xu and Ding, 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">Shrinkage Baselines</b><span class="text-[8px] text-slate-500">(Zeng et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">Optimal Baseline</b><span class="text-[8px] text-slate-500">(Hao et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">Rollout Down-Sampling</b><span class="text-[8px] text-slate-500">(Xu et al., 2025)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">EBPO</b><span class="text-[8px] text-slate-500">(Han et al., 2026)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">RiskPO</b><span class="text-[8px] text-slate-500">(Ren et al., 2026)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">BASIS</b><span class="text-[8px] text-slate-500">(Gong et al., 2026a)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">KAE</b><span class="text-[8px] text-slate-500">(Gong et al., 2026b)</span></div>
<div class="h-[35px] rounded-lg border border-blue-100 bg-white flex flex-col justify-center"><b class="text-[10px]">BiCC</b><span class="text-[8px] text-slate-500">(Li et al., 2026)</span></div>
<div class="h-[35px] flex items-center justify-center text-2xl font-bold tracking-[0.25em] text-blue-400">...</div>
</div>
</div>

<div class="col-span-2 rounded-2xl border-2 border-violet-200 bg-violet-50/40 p-3">
<div class="mb-2 text-center text-[13px] font-bold uppercase tracking-wide text-violet-800">Theory & Analysis</div>
<div class="grid grid-cols-1 gap-1 text-center">
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">What Is the Alignment Objective of GRPO?</b><span class="text-[8px] text-slate-500">(Vojnovic and Yun, 2025)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">What Is the Objective of Reasoning with RL?</b><span class="text-[8px] text-slate-500">(Davis and Recht, 2025)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">Theory and Practice of GRPO</b><span class="text-[8px] text-slate-500">(Pang and Jin, 2025)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">GRPO Is Secretly DPO</b><span class="text-[8px] text-slate-500">(Wu et al., 2025)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">Your Group-Relative Advantage Is Biased</b><span class="text-[8px] text-slate-500">(Yang et al., 2026)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">Group-Relative REINFORCE Is Off-Policy</b><span class="text-[8px] text-slate-500">(Yao et al., 2026)</span></div>
<div class="h-[35px] px-2 rounded-lg border border-violet-100 bg-white flex flex-col justify-center"><b class="text-[9px] leading-3">Demystifying GRPO</b><span class="text-[8px] text-slate-500">(Zhou et al., 2026)</span></div>
<div class="h-[35px] flex items-center justify-center text-2xl font-bold tracking-[0.25em] text-violet-400">...</div>
</div>
</div>

</div>
---

# A Practical Reasoning Post-Training Recipe

<div class="grid grid-cols-2 gap-8 mt-6">

<div>

## Data and rewards

1. Start with a model that can follow instructions.
2. Use a small amount of high-quality reasoning data if readability matters.
3. Sample multiple responses per prompt.
4. Score with verifiers where possible.
5. Use preference data where correctness is not directly verifiable.

</div>

<div>

## Optimization

1. Convert rewards into advantages.
2. Use group or leave-one-out baselines.
3. Stabilize long responses with sequence-level control when needed.
4. Keep KL/reference control only when it is doing useful work.
5. Monitor length, diversity, calibration, and reward hacking.

</div>

</div>


---

# Example: AI Detection

<div class="mt-2 text-[14px] leading-5.5 text-slate-700 text-center">
Given a text <MathTex tex="x" />, READER generates a structured rationale <MathTex tex="c" /> before predicting the authorship label <MathTex tex="y\in\{\mathrm{Human},\mathrm{AI}\}" />.
</div>

<div class="flex justify-center mt-3">
<img src="/figs/reader-compare.png" class="w-full h-[270px] object-contain" />
</div>

<div class="grid grid-cols-3 gap-4 mt-3 text-[11px] leading-4.5">
<div class="px-3 py-2.5 rounded-xl border-2 border-blue-200 bg-blue-50">
<div class="text-[10px] uppercase tracking-wide text-blue-700 font-bold mb-1">READ Supervision</div>
<b>19,684</b> rationale demonstrations and <b>77,103</b> answer-only instances across diverse domains and generators.
</div>
<div class="px-3 py-2.5 rounded-xl border-2 border-emerald-200 bg-emerald-50">
<div class="text-[10px] uppercase tracking-wide text-emerald-700 font-bold mb-1">Training</div>
Start from <b>Qwen2.5-1.5B-Instruct</b>: use SFT to learn structured explanations, then GRPO to improve detection accuracy.
</div>
<div class="px-3 py-2.5 rounded-xl border-2 border-orange-200 bg-orange-50">
<div class="text-[10px] uppercase tracking-wide text-orange-700 font-bold mb-1">Key Result</div>
More than <b>20 percentage points</b> above prompted flagship LLMs while being <b>100--1,000× smaller</b>.
</div>
</div>

<div class="absolute bottom-2 left-12 right-12 text-[8px] leading-3 text-slate-400 text-center">
Pingfan Su, Kai Ye, Shijin Gong, Erhan Xu, Jin Zhu, Giulia Livieri, and Chengchun Shi. "READER: Reasoning-Enhanced AI-Generated Text Detection." arXiv preprint arXiv:2605.25281 (2026).
</div>


---
layout: center
class: text-center
---

# Thank You!

<div class="pt-12">
  <span class="text-6xl">🤖</span>
</div>

<div class="pt-8 text-xl">
  Explore the Infinite Possibilities of LLMs
</div>

<div class="abs-br m-6 flex gap-2">
  <a href="https://noncollapse.github.io/" target="_blank" alt="GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>
