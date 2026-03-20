const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['OLIVE', 'Olive', '王子', 'prince', 'little prince', 'Little Prince', '海之戀 餐廳', '西餐 推薦', 'brunch', 'Brunch', '意粉', '牛排', '羊架'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：OLIVE / Little Prince / 王子廚房 (西餐)');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const foodRelevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('食') || t.includes('好') || t.includes('推薦') || t.includes('價錢') || t.includes('價') || t.includes('$') || t.includes('味') || t.includes('餐') || t.includes('意粉') || t.includes('牛');
    });
    
    console.log('=== OLIVE / Little Prince / 西餐相關記錄 ===');
    console.log('');
    foodRelevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到相關討論');
}
