const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['little prince', 'Little Prince', '王子', '海之戀 餐廳', 'OLIVE', 'Olive'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：Little Prince / 王子餐廳');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    console.log('=== Little Prince / 王子餐廳相關記錄 ===');
    console.log('');
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到 Little Prince / 王子餐廳相關討論');
}
