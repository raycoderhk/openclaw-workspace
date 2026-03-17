const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['cafe', '咖啡', 'café', 'coffee', '星巴克', 'starbucks', '太平洋咖啡', 'Pacific Coffee', '茶記', '冰室', '甜品', 'cottage', 'theatre cafe'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：Cafe / 咖啡店');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const relevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('愉景') || t.includes('荃灣') || t.includes('D-PARK') || t.includes('D PARK') || t.includes('DPARK') || t.includes('推薦') || t.includes('好') || t.includes('開') || t.includes('新');
    });
    
    console.log('=== Cafe / 咖啡店相關記錄 ===');
    console.log('');
    relevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到 Cafe 相關討論');
}
