const LECT = { label: 'Lecture 0 · the big shift', title: 'From Chatbots to Agents' };
const LAYERS = ['Who starts the work', 'How long it lives', 'What it can touch', 'What done means'];
say({
  hook: "You ask a chatbot a question. It answers. Then it forgets you exist until you type again. Now picture something different: an assistant that notices your flight got cancelled at three in the morning, rebooks you, and messages you before you wake up. Same model underneath. Completely different system.",
  title: "This course is about long running and personal agents: what they are, how they're built behind the scenes, what to watch out for when you build one, and how people actually test them. In this first lecture, we'll pin down exactly what changes when a chatbot becomes an agent.",
  recap: "To recap. A chatbot is a function you call. An agent is a process that lives somewhere. It can start work by itself, it runs for days or months, it holds real credentials and takes real actions, and done means the world is in the right state, not that it replied.",
  outro: "Next, we'll meet the four agents everyone's talking about right now: OpenAI dots, Meta Muse, Grok Bot, and OpenClaw.",
});
intro('S01_Intro', 'hook', 'title', [
  ['flow', ['you ask', 'it answers', 'it forgets'], ['w', 'g', 'gr'], { at: 'question' }],
  ['text', '3 a.m.: flight cancelled → rebooked → you get a message', 'o', 44, { at: 'notices' }],
  ['big', 'Same model. Different system.', 'y', 70, { at: 'Same' }],
]);
section('S02_Who', 0, 'v', [
  { b: 'wh1', t: 'A function vs a process', say: "Here's the one sentence version. A chatbot is a function you call: input goes in, an answer comes out, done. An agent is a process: it lives somewhere, keeps state, and keeps running whether or not you're watching.", v: [
    ['row', [['col', 'chatbot', 'b', ['a function you call', 'in → out → done']], ['col', 'agent', 'g', ['a process that lives', 'keeps state, keeps running']]], { vs: true, times: [['wh1', .2, 'f'], ['wh1', .55, 'f']] }],
  ] },
  { b: 'wh2', t: 'Who presses go?', say: "So the first big difference is who starts the work. With a chatbot, it's always you, every single turn. An agent can also be woken by a schedule, by an event like a new email, or by its own heartbeat, a timer that makes it check whether anything needs doing.", v: [
    ['flow', ['you', 'schedule', 'new email', 'heartbeat'], ['w', 'y', 'b', 'p'], { times: [['wh2', .3, 'f'], ['wh2', .55, 'f'], ['wh2', .65, 'f'], ['wh2', .78, 'f']] }],
    ['note', 'heartbeat: a timer that asks "anything to do?"', 'p', { at: 'timer' }],
  ] },
  { b: 'wh3', t: 'Like an employee, not a vending machine', say: "Think of a vending machine versus an employee. The vending machine only acts when you press a button. A good employee notices things and handles them while you're busy elsewhere.", v: [
    ['analogy', null, 'a vending machine waits for a button; an employee notices things', 'o', { at: 'vending' }],
  ] },
]);
section('S03_Lives', 1, 'b', [
  { b: 'li1', t: 'Seconds vs months', say: "Second difference: lifetime. A chatbot request lives for seconds. An agent's task can live for days, and the agent itself for months. So it needs durable state: memory, files, logins, even a whole computer of its own that stays switched on.", v: [
    ['timeline', [['seconds', 'a chatbot reply', 'b'], ['days', 'one agent task', 'y'], ['months', 'the agent itself', 'g']], { times: [['li1', .1, 'f'], ['li1', .25, 'f'], ['li1', .35, 'f']] }],
    ['tokens', ['memory', 'files', 'logins', 'its own computer'], 'g', { at: 'durable', step: .5 }],
  ] },
]);
section('S04_Touch', 2, 'p', [
  { b: 'to1', t: 'Words vs actions', say: "Third: what it can touch. A chatbot's output is text. If it's wrong, you shrug and ask again. An agent sends email, spends money, edits code. Its mistakes are actions, and some can't be undone.", v: [
    ['row', [['col', 'chatbot output', 'b', ['text']], ['col', 'agent output', 'p', ['emails', 'payments', 'code commits']]], { vs: true, times: [['to1', .15, 'f'], ['to1', .5, 'f']] }],
    ['note', "some actions can't be undone", 'p', { at: "can't" }],
  ] },
  { b: 'to2', t: 'A real cautionary tale', say: "This isn't hypothetical. One OpenClaw user lost around six thousand emails after a prompt injection, hidden instructions inside content the agent read, told it to delete them. A chatbot can only say something wrong. An agent can do something wrong.", v: [
    ['eq', '≈ 6,000 emails deleted', 'p', { at: 'thousand' }],
    ['text', 'cause: hidden instructions inside content it read', 'gr', 36, { at: 'hidden' }],
    ['big', 'say wrong  vs  do wrong', 'y', 60, { at: 'chatbot' }],
  ] },
  { b: 'to3', t: 'It has its own identity', say: "Which is why an agent gets its own identity: its own accounts, its own credentials, and its own permissions. Think of it as a new hire, not a tool.", v: [
    ['list', ['own accounts', 'own credentials', 'own permissions'], 'p', { tick: true, times: [['to3', .3, 'f'], ['to3', .45, 'f'], ['to3', .6, 'f']] }],
  ] },
]);
section('S05_Done', 3, 'g', [
  { b: 'dn1', t: 'What does done mean?', say: "And finally, what counts as done. For a chatbot, done means it replied. For an agent, done means the world is now in the right state, the booking really exists, and also that it didn't do anything it shouldn't have.", v: [
    ['row', [['col', 'chatbot: done =', 'b', ['it replied']], ['col', 'agent: done =', 'g', ['the world is right', 'and nothing bad happened']]], { vs: true, times: [['dn1', .1, 'f'], ['dn1', .3, 'f']] }],
  ] },
  { b: 'dn2', t: 'Everything hard comes from this', say: "So ultimately, the model might be the same. But every hard problem in this course, architecture, memory, safety, and testing, comes from that one change: from a function you call, to a process that acts for you.", v: [
    ['tokens', ['architecture', 'memory', 'safety', 'testing'], 'y', { at: 'architecture', step: .5 }],
    ['big', 'function you call → process that acts', 'o', 58, { at: 'function' }],
  ] },
]);
recap('S06_Recap', 'recap', 'outro', ['it can start work itself', 'lives for days or months', 'holds credentials, takes actions', 'done = the world is right'], 'The agent landscape');
