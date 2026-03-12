import fs from 'fs';
import path from 'path';

// WhatsApp export format: [DD/M/YYYY, HH:MM:SS] Sender: Message
const WHATSAPP_REGEX = /^\[(\d{1,2}\/\d{1,2}\/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)$/;

// Noise patterns to filter out
const NOISE_PATTERNS = [
  /sticker omitted/i,
  /image omitted/i,
  /video omitted/i,
  /audio omitted/i,
  /This message was deleted/i,
  /created this group/i,
  /joined using a group link/i,
  /Messages and calls are end-to-end encrypted/i,
  /^\.$/,  // Single dot
  /^\?$/,  // Single question mark
  /^!$/,   // Single exclamation
  /^\.$/,  // Single character replies
  /^\w$/,  // Single character
  /^[\u4e00-\u9fff]$/,  // Single Chinese character
];

function parseChatFile(inputPath, outputPath) {
  console.log(`📖 Reading ${inputPath}...`);
  const content = fs.readFileSync(inputPath, 'utf-8');
  const lines = content.split('\n');
  
  const messages = [];
  let skipped = 0;
  let noise = 0;
  
  for (const line of lines) {
    if (!line.trim()) continue;
    
    const match = line.match(WHATSAPP_REGEX);
    if (!match) {
      skipped++;
      continue;
    }
    
    const [, dateStr, timeStr, sender, text] = match;
    
    // Parse date [DD/M/YYYY]
    const [day, month, year] = dateStr.split('/').map(Number);
    const msgDate = new Date(year, month - 1, day);
    
    // Parse time [HH:MM:SS]
    const [hour, minute, second] = timeStr.split(':').map(Number);
    msgDate.setHours(hour, minute, second);
    
    // Check if noise
    const isNoise = NOISE_PATTERNS.some(pattern => pattern.test(text));
    if (isNoise) {
      noise++;
      continue;
    }
    
    messages.push({
      date: msgDate.toISOString().split('T')[0], // YYYY-MM-DD
      time: timeStr,
      datetime: msgDate.toISOString(),
      sender: sender.trim(),
      text: text.trim(),
      raw: line
    });
  }
  
  console.log(`✅ Parsed ${messages.length} useful messages`);
  console.log(`⏭️  Skipped ${skipped} malformed lines`);
  console.log(`🗑️  Filtered ${noise} noise messages`);
  console.log(`📊 Noise ratio: ${(noise / lines.length * 100).toFixed(1)}%`);
  
  // Write parsed output
  fs.writeFileSync(outputPath, JSON.stringify(messages, null, 2));
  console.log(`💾 Saved to ${outputPath}`);
  
  // Extract unique senders
  const senders = [...new Set(messages.map(m => m.sender))];
  const sendersPath = outputPath.replace('.json', '_senders.json');
  fs.writeFileSync(sendersPath, JSON.stringify(senders.sort(), null, 2));
  console.log(`👥 Found ${senders.length} unique senders → ${sendersPath}`);
  
  return messages;
}

// Main
const inputPath = process.argv[2] || './raw/_chat.txt';
const outputPath = process.argv[3] || './output/parsed_messages.json';

// Ensure output directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

parseChatFile(inputPath, outputPath);
