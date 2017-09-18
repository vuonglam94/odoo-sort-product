odoo.define('sort_product.db', function (require) {
"use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var db = require('point_of_sale.DB');

    db.include({
        get_product_by_category_ids: function(category_id, recommended_ids){
            var product_ids  = this.product_by_category_id[category_id];
            var temp = [];
            var list_ids = recommended_ids;
            for (var i = 0; i < list_ids.length; i++) {
                if (product_ids.includes(list_ids[i])) {
                    temp.push(list_ids[i])
                }
            }
            for (var i = 0; i < product_ids.length; i++) {
                if (!(temp.includes(product_ids[i]))) {
                    temp.push(product_ids[i])
                }
            }
            var list = [];
//            console.log('temp');
//            console.log(temp);
            if (temp) {
                for (var i = 0, len = Math.min(temp.length, this.limit); i < len; i++) {
                    list.push(this.product_by_id[temp[i]]);
                }
            }
//            console.log('list');
//            console.log(list);
            return list;
        },
    });
});