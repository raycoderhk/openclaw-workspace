const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['健身室', 'gym room', 'gym 房', 'fitness room', '會所 gym', '會所健身', '重量', '器械', '跑步機', 'fitness'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：健身室 / Gym Room');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    matches.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 200));
        console.log('');
    });
} else {
    console.log('❌ 未找到健身室相關討論');
    console.log('');
    console.log('💡 社區可能未詳細討論過健身室');
}
