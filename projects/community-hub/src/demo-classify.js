import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// Demo: Classify just 50 messages to show the user what output looks like

const CATEGORIES = {
  traffic: 'Traffic & Transport (accidents, bus routes, taxi, MTR tips)',
  restaurant: 'Restaurants & Food (recommendations, OpenRice links, deals)',
  doctor: 'Doctors & Medical (clinics, recommendations, health tips)',
  tech_tip: 'Tech Tips (phone plans, apps, gadgets, comparisons)',
  shopping: 'Shopping & Deals (promo codes, coupons, where to buy)',
  service: 'Services (delivery, logistics, repairs, rentals)',
  community: 'Community & Estate (management, facilities, issues)',
  event: 'Events & Activities (BBQ, gatherings, sports, classes)',
  news: 'News & Articles (local news, school info, important updates)',
  repair: 'Home Repairs (plumbers, electricians, AC, locksmith)',
  education: 'Education (tutors, schools, courses, materials)',
  childcare: 'Childcare & Kids (toys, schools, activities, parenting tips)',
};

function buildPrompt(messages) {
  return `You are classifying WhatsApp messages from a Hong Kong neighborhood community group (愉景新城/愉城).

CATEGORIES:
${Object.entries(CATEGORIES).map(([key, desc]) => `- ${key}: ${desc}`).join('\n')}

RULES:
1. Only mark as "useful: true" if the message contains actionable information (recommendations, tips, alerts, links to resources)
2. Casual chat, greetings, jokes, opinions without facts → useful: false
3. Extract entity names (businesses, people, places, products)
4. Summarize in English (concise, 1 line)
5. Detect language: "zh" (Chinese), "en" (English), "mixed"

Return a JSON array. Each item:
{
  "index": <original array index>,
  "category": "<one category or null if noise>",
  "useful": true/false,
  "summary": "<English summary, only if useful=true>",
  "entities": ["<extracted names>"],
  "language": "zh" | "en" | "mixed"
}

MESSAGES TO CLASSIFY:
${messages.map((m, i) => `[${i}] [${m.date} ${m.time}] ${m.sender}: ${m.text}`).join('\n')}

Respond with ONLY the JSON array, no other text.`;
}

async function classifyBatch(messages, apiKey) {
  const prompt = buildPrompt(messages);
  
  const response = await fetch('https://coding.dashscope.aliyuncs.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'qwen3.5-plus',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.1,
      max_tokens: 2000
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  
  const data = await response.json();
  const content = data.choices[0].message.content;
  
  const jsonMatch = content.match(/\[[\s\S]*\]/);
  if (!jsonMatch) {
    console.error('Failed to parse JSON:', content);
    return null;
  }
  
  return JSON.parse(jsonMatch[0]);
}

async function demo() {
  console.log('🎬 Community Hub - Demo Classification\n');
  
  const apiKey = process.env.ALIYUN_API_KEY;
  if (!apiKey) {
    console.error('❌ Set ALIYUN_API_KEY first');
    console.error('   export ALIYUN_API_KEY=your_key_here');
    process.exit(1);
  }
  
  // Load parsed messages
  const allMessages = JSON.parse(fs.readFileSync('./output/parsed_messages.json', 'utf-8'));
  console.log(`📊 Total parsed messages: ${allMessages.length}`);
  
  // Select diverse sample: 50 messages from different dates
  const sampleSize = 50;
  const step = Math.floor(allMessages.length / sampleSize);
  const sample = [];
  for (let i = 0; i < allMessages.length && sample.length < sampleSize; i += step) {
    sample.push(allMessages[i]);
  }
  
  console.log(`🎯 Selected ${sample.length} diverse messages for demo\n`);
  
  // Show sample messages
  console.log('📋 Sample Messages:\n');
  for (let i = 0; i < Math.min(10, sample.length); i++) {
    const m = sample[i];
    console.log(`[${i+1}] [${m.date}] ${m.sender}: ${m.text.substring(0, 80)}${m.text.length > 80 ? '...' : ''}`);
  }
  console.log('... and more\n');
  
  // Classify
  console.log('🤖 Classifying with DeepSeek AI...\n');
  const results = await classifyBatch(sample, apiKey);
  
  if (!results) {
    console.error('❌ Classification failed');
    return;
  }
  
  // Merge results
  const classified = results.map(r => ({
    ...sample[r.index],
    category: r.category,
    useful: r.useful,
    summary: r.summary,
    entities: r.entities,
    language: r.language
  }));
  
  // Show results
  console.log('✅ Classification Results:\n');
  
  const useful = classified.filter(r => r.useful && r.category);
  const notUseful = classified.filter(r => !r.useful || !r.category);
  
  console.log(`📊 Summary:`);
  console.log(`   Useful tips: ${useful.length}/${classified.length} (${(useful.length/classified.length*100).toFixed(0)}%)`);
  console.log(`   Not useful: ${notUseful.length}\n`);
  
  console.log('🏷️  By Category:');
  const catCounts = {};
  for (const r of useful) {
    catCounts[r.category] = (catCounts[r.category] || 0) + 1;
  }
  for (const [cat, count] of Object.entries(catCounts).sort((a, b) => b[1] - a[1])) {
    console.log(`   ${cat}: ${count}`);
  }
  
  console.log('\n💡 Sample Useful Tips:\n');
  for (const tip of useful.slice(0, 5)) {
    console.log(`📌 [${tip.category}] ${tip.date}`);
    console.log(`   ${tip.text}`);
    console.log(`   → ${tip.summary}`);
    console.log(`   Entities: ${tip.entities.join(', ')}`);
    console.log();
  }
  
  // Save demo output
  fs.writeFileSync('./output/demo_classified.json', JSON.stringify(classified, null, 2));
  console.log('💾 Saved demo results to ./output/demo_classified.json');
  
  // Estimate full cost
  const totalBatches = Math.ceil(allMessages.length / 25);
  const estimatedCost = totalBatches * 0.0005;
  console.log(`\n💰 Full Dataset Estimate:`);
  console.log(`   Messages: ${allMessages.length}`);
  console.log(`   Batches: ${totalBatches} (25 messages/batch)`);
  console.log(`   Estimated cost: $${estimatedCost.toFixed(2)} USD (DeepSeek via OpenRouter)`);
}

demo();
