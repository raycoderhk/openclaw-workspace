const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['上網', '寬頻', '網上行', 'HGC', 'HKBN', 'PCCW', '中國移動', 'CMHK', '數據', '月費', '寬頻', '光纖', '1000M', '2000M', '5G', '4G', 'SIM', '電話卡', '流量'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：上網 / 寬頻 價錢');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const priceRelevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('$') || t.includes('元') || t.includes('月費') || t.includes('價錢') || t.includes('費') || t.includes('M') || t.includes('GB');
    });
    
    console.log('=== 上網 / 寬頻價錢相關記錄 ===');
    console.log('');
    priceRelevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到上網價錢相關討論');
}
