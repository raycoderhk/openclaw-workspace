const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['Cottage', 'Theatre Cafe', 'Food Court', '美食廣場', '麥當勞', 'McDonald', '大家樂', '大快活', '吉野家', '肯德基', 'KFC', '星巴克', 'Starbucks', 'McCafe', '太平洋咖啡'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：Cottage / Theatre Cafe / 美食廣場');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    console.log('=== Cottage / Theatre Cafe / 美食廣場相關記錄 ===');
    console.log('');
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到相關討論');
}
