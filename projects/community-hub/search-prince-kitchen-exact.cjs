const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

// Search for 王子廚房 specifically
const keywords = ['王子廚房', 'Prince Kitchen', 'prince kitchen', '王子', 'Kitchen'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    // More specific match - must have both 王子 and 廚房 or be directly about the restaurant
    return text.includes('王子廚房') || 
           (text.includes('王子') && (text.includes('廚房') || text.includes('Kitchen') || text.includes('restaurant'))) ||
           text.toLowerCase().includes('prince kitchen');
});

console.log('🔍 搜索：王子廚房 (Prince Kitchen)');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    console.log('=== 王子廚房相關記錄 ===');
    console.log('');
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 300));
        console.log('');
    });
} else {
    console.log('❌ 未找到王子廚房直接討論');
    console.log('');
    console.log('💡 社區可能未討論過王子廚房，但圖片顯示這是一間餐廳');
    console.log('');
    console.log('📸 用戶分享的圖片顯示王子廚房菜單/介面');
}
