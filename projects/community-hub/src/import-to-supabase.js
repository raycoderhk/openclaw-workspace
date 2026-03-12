import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

async function importToSupabase(inputPath) {
  // Load environment variables
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_ANON_KEY;
  
  if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing Supabase credentials');
    console.error('   Set: SUPABASE_URL and SUPABASE_ANON_KEY');
    process.exit(1);
  }
  
  const supabase = createClient(supabaseUrl, supabaseKey);
  
  console.log(`📖 Loading classified messages from ${inputPath}...`);
  const messages = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
  const usefulMessages = messages.filter(m => m.useful && m.category);
  
  console.log(`📊 Importing ${usefulMessages.length} useful tips to Supabase...`);
  
  const BATCH_SIZE = 100;
  let imported = 0;
  let errors = 0;
  
  for (let i = 0; i < usefulMessages.length; i += BATCH_SIZE) {
    const batch = usefulMessages.slice(i, i + BATCH_SIZE);
    const batchNum = Math.floor(i / BATCH_SIZE) + 1;
    const totalBatches = Math.ceil(usefulMessages.length / BATCH_SIZE);
    
    // Transform for Supabase
    const records = batch.map(m => ({
      msg_date: m.date,
      msg_time: m.time,
      datetime: m.datetime,
      sender: m.sender,
      raw_text: m.text,
      category: m.category,
      useful: true,
      summary_en: m.summary || null,
      entities: m.entities || [],
      language: m.language || 'mixed'
    }));
    
    console.log(`\n🔄 Importing batch ${batchNum}/${totalBatches}...`);
    
    const { data, error } = await supabase
      .from('community_tips')
      .insert(records)
      .select();
    
    if (error) {
      console.error(`❌ Batch ${batchNum} error:`, error.message);
      errors++;
    } else {
      imported += data.length;
      console.log(`✅ Batch ${batchNum} imported: ${data.length} records`);
    }
    
    // Rate limiting
    if (i + BATCH_SIZE < usefulMessages.length) {
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
  
  console.log(`\n📊 Import Summary:`);
  console.log(`   Successfully imported: ${imported}`);
  console.log(`   Errors: ${errors}`);
  console.log(`   Success rate: ${(imported / usefulMessages.length * 100).toFixed(1)}%`);
  
  // Verify import
  console.log(`\n🔍 Verifying import...`);
  const { count, error: countError } = await supabase
    .from('community_tips')
    .select('*', { count: 'exact', head: true });
  
  if (countError) {
    console.error('❌ Verification failed:', countError.message);
  } else {
    console.log(`✅ Total records in database: ${count}`);
  }
  
  // Show category stats
  const { data: stats, error: statsError } = await supabase
    .rpc('tips_stats');
  
  if (statsError) {
    console.error('⚠️  Could not fetch stats:', statsError.message);
  } else {
    console.log(`\n📁 Category Statistics:`);
    for (const stat of stats || []) {
      console.log(`   ${stat.category}: ${stat.total_count} total, ${stat.last_7_days} this week`);
    }
  }
}

// Main
const inputPath = process.argv[2] || './output/classified_messages_useful.json';

importToSupabase(inputPath);
