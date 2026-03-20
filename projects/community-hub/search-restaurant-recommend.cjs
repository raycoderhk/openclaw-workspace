const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['海之戀', '海戀', '荃灣 餐廳', '荃灣 食', '南豐', '南豐中心', '餐廳推薦', '食飯推薦', '西餐', 'brunch', 'Brunch'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：海之戀 / 荃灣 餐廳推薦');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    console.log('=== 海之戀 / 荃灣 餐廳推薦記錄 ===');
    console.log('');
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到相關討論');
}
