const LECT = { label: 'Bonus 4 · beyond the book', title: 'Deterministic Inference' };
const LAYERS = ['The experiment', 'The cause', 'The fix', 'Why bother'];
say({
  hook: "Set temperature to zero, which should mean no randomness at all. Ask a model the exact same question a thousand times. How many different answers do you get? One? In a famous experiment, the answer was eighty.",
  title: "This bonus lecture is about deterministic inference: why the same input can give different outputs, and how to make a model give exactly the same answer every time.",
  recap: "To recap. Temperature zero isn't enough for determinism. Adding numbers in a different order changes the last few digits, and the order depends on how many other users share the batch. Batch invariant kernels fix the order, at a cost that keeps shrinking. Use it for debugging, testing and reinforcement learning.",
  outro: "Last bonus: diffusion language models, which write text a whole new way.",
});
intro('S01_Intro', 'hook', 'title', [
  ['eq', 'temperature = 0', 'b', { at: 'temperature' }],
  ['people', 20, 'gr', 'same question × 1,000', { at: 'thousand' }],
  ['big', '80 different answers', 'p', 80, { at: 'eighty' }],
]);
section('S02_Experiment', 0, 'v', [
  { b: 'ex1', t: 'The experiment', cite: 'Thinking Machines Lab, Sept 2025', say: "Researchers at Thinking Machines Lab asked Qwen3 two thirty five B to tell them about Richard Feynman, a thousand times, at temperature zero. The answers were identical for the first hundred and two tokens. Then, at token one hundred and three, they split: nine hundred ninety two said Queens, New York, and eight said New York City. In total: eighty different completions.", v: [
    ['tokens', ['token 1', '…', 'token 102', 'token 103'], 'g', { times: [['ex1', .4, 'f'], ['ex1', .45, 'f'], ['ex1', .5, 'f'], ['ex1', .58, 'f']], cols: [0, 0, 0, 'y'] }],
    ['hbars', [['"Queens, New York"', 992, 'g', '992'], ['"New York City"', 8, 'p', '8']], { times: [['ex1', .68, 'f'], ['ex1', .78, 'f']], lw: 420 }],
    ['eq', '80 different completions', 'p', { at: 'total' }],
  ] },
]);
section('S03_Cause', 1, 'p', [
  { b: 'ca1', t: 'Computers round as they add', say: "Why? Start with a surprising fact: on a computer, adding decimal numbers in a different order can give a slightly different result, because every step rounds a little. Add a tiny number to a huge one, and the tiny one can vanish.", v: [
    ['eq', '(a + b) + c ≠ a + (b + c)', 'y', { at: 'different' }],
    ['analogy', null, 'adding a grain of sand to a truckload: the scale does not notice', 'o', { at: 'tiny' }],
  ] },
  { b: 'ca2', t: 'The real culprit: other users', say: "The popular explanation was parallel threads racing each other. But the researchers found the real culprit: batch size. The GPU picks how to split up its additions based on how many requests are in the batch. And that depends on how busy the server is, which depends on everyone else's traffic. So your answer depends on other people's requests.", v: [
    ['text', '"threads racing each other"', 'p', 44, { at: 'popular' }],
    ['flow', ['how busy the server is', 'how additions are split', 'your exact answer'], ['y', 'p', 'w'], { at: 'GPU' }],
    ['note', 'your answer depends on other people\'s traffic', 'o', { at: 'depends', occ: 2 }],
  ] },
]);
section('S04_Fix', 2, 'g', [
  { b: 'fx1', t: 'The fix: batch invariance', say: "The fix is called batch invariance: rewrite the key kernels, normalisation, matrix multiplication, and attention, so each request's additions happen in exactly the same order, whatever the batch size.", v: [
    ['text', 'same addition order, whatever the batch size', 'g', 46, { at: 'same' }],
    ['tokens', ['normalisation', 'matrix multiply', 'attention'], 'y', { at: 'normalisation', step: 1 }],
  ] },
  { b: 'fx2', t: 'It works, at a cost', say: "With these kernels, a thousand runs gave a thousand identical answers. The cost: on Qwen3 eight B in vLLM, the default took twenty six seconds, the first deterministic version fifty five, and an improved one forty two. Slower, but the gap keeps closing.", v: [
    ['eq', '1,000 runs → 1 answer', 'g', { at: 'thousand' }],
    ['hbars', [['default', 26, 'gr', '26 s'], ['first version', 55, 'p', '55 s'], ['improved', 42, 'y', '42 s']], { times: [['fx2', .6, 'f'], ['fx2', .75, 'f'], ['fx2', .88, 'f']], lw: 330 }],
  ] },
]);
section('S05_Why', 3, 'o', [
  { b: 'wh1', t: 'Why pay for it?', say: "Why pay that cost? Two reasons. Reproducible debugging and testing: when a bug appears, you can replay it exactly. And reinforcement learning, where the model that generates answers and the model that learns from them must agree, bit for bit. vLLM now offers this as a simple switch: a setting called VLLM batch invariant, set to one.", v: [
    ['list', ['replay bugs exactly', 'reinforcement learning: generator and learner agree bit for bit'], 'o', { num: true, times: [['wh1', .15, 'f'], ['wh1', .45, 'f']] }],
    ['card', 'in vLLM', [['setting'], ['VLLM_BATCH_INVARIANT=1']], { w: 760 }, { at: 'switch' }],
  ] },
]);
recap('S06_Recap', 'recap', 'outro', ['temperature 0 isn\'t deterministic', 'addition order follows batch size', 'batch-invariant kernels fix it', 'worth it for debugging + RL'], 'Diffusion language models');
