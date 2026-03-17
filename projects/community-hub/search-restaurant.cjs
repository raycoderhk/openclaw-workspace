const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['餐廳', '食肆', '食飯', '茶餐廳', '冰室', '快餐', '美食', '美食廣場', 'food court', 'court', 'D-PARK', 'DPARK', 'D PARK', '商場 食', '樓下 食', '愉景 食'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：餐廳 / 美食廣場');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const relevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('推薦') || t.includes('好') || t.includes('新') || t.includes('開') || t.includes('关闭') || t.includes('结业') || t.includes('搬') || t.includes('$') || t.includes('元') || t.includes('價');
    });
    
    console.log('=== 餐廳 / 美食廣場相關記錄 (前 30 條) ===');
    console.log('');
    relevant.sort((a, b) => a.date.localeCompare(b.date)).slice(0, 30).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到餐廳相關討論');
}
