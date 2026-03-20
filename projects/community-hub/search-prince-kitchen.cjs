const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['王子', '廚房', '王子廚房', 'prince', 'cook', 'chef', '餐廳', '食肆'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：王子廚房');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    console.log('=== 王子廚房相關記錄 ===');
    console.log('');
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到王子廚房相關討論');
    console.log('');
    console.log('💡 社區可能未討論過王子廚房');
}
