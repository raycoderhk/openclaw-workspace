const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['HKBN', 'hkbn', '網上行', 'HGC', 'PCCW', 'pccw', '中國移動', 'CMHK', 'csl', 'CSL', 'SoSIM', 'ClubSIM', '3HK', '寬頻', '光纖', '1000M', '2000M', '5G', '4G', '月費', '$89', '$99', '$179', '$228'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：ISP / 電訊商 價錢');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const priceRelevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('$') || t.includes('月費') || t.includes('M') || t.includes('GB') || t.includes('寬頻') || t.includes('數據');
    });
    
    console.log('=== ISP / 電訊商價錢記錄 ===');
    console.log('');
    priceRelevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到電訊商價錢討論');
}
