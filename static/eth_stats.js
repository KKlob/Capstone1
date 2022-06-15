/** Handles updating the eth_stats on main page */

const $total_eth = $('#total_supply')
const $total_eth2 = $('#total_supply_eth2')
const $last_price = $('#last_price')
const $sg_gwei = $('#sg_gwei')
const $sg_conf = $('#sg_conf')
const $pg_gwei = $('#pg_gwei')
const $pg_conf = $('#pg_conf')
const $fg_gwei = $('#fg_gwei')
const $fg_conf = $('#fg_conf')
const $base_fee = $('#base_fee')

async function update_stats() {
    stats = await get_stats();
    let ts = String(BigInt(stats['total_supply']))
    let ts2 = String(BigInt(stats['total_supply_eth2']))
    let lp = String("$" + stats['last_price'])
    let sg = stats['safe_gas']
    let pg = stats['prop_gas']
    let fg = stats['fast_gas']

    $total_eth.text(format_supply(ts))
    $total_eth2.text(format_supply(ts2))
    $last_price.text(lp)

    $sg_gwei.text(sg['gwei'])
    $sg_conf.text(sg['est_conf'])

    $pg_gwei.text(pg['gwei'])
    $pg_conf.text(pg['est_conf'])

    $fg_gwei.text(fg['gwei'])
    $fg_conf.text(fg['est_conf'])

    $base_fee.text(stats['base_fee'])
}

async function get_stats() {
    resp = await axios.get('/api/get_eth_stats');
    stats = resp['data'];
    return stats
}

function format_supply(str) {
    str_array = str.split('')
    count = 0
    for (let i = str_array.length - 1; i >= 0; i--) {
        count++;
        if (count == 3) {
            if (i !== 0) {
                str_array.splice(i, 0, ",");
                count = 0;
            }
        }
    }
    str = str_array.join('')
    return str
}

update_stats()
setInterval(update_stats, 12000)