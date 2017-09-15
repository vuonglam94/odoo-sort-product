odoo.define('sort_product.db', function (require) {
"use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var db = require('point_of_sale.DB');

    db.include({
        get_product_by_ids: function(ids){
            var product_ids  = ids;
            console.log(ids);
            var list = [];
            if (product_ids) {
                for (var i = 0; i < product_ids.length; i++) {
                    list.push(this.product_by_id[product_ids[i]]);
                }
            }
            console.log('aasdasdasdasd');
            console.log(list);
            return list;
        },
    });
});