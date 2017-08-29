odoo.define('sort_product.screens', function (require) {
"use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var screens = require('point_of_sale.screens');

    screens.ProductListWidget.include({
        renderElement: function() {
            var el_str  = QWeb.render(this.template, {widget: this});
            var el_node = document.createElement('div');
                el_node.innerHTML = el_str;
                el_node = el_node.childNodes[1];

            if(this.el && this.el.parentNode){
                this.el.parentNode.replaceChild(el_node,this.el);
            }
            this.el = el_node;
            var list_container = el_node.querySelector('.product-list');
            this.product_list.sort(function (a,b) {
                return b.qty - a.qty;
            });
            for(var i = 0, len = this.product_list.length; i < len; i++){
                var product_node = this.render_product(this.product_list[i]);
                product_node.addEventListener('click',this.click_product_handler);
                list_container.appendChild(product_node);
            }
//            console.log(this.product_list);
//            console.log(this.product_list.length);
//            console.log(this.product_list[0]);
//            console.log(this.product_list[0].qty);
//            for (var i = 0; i < this.product_list.length; i++){
//                console.log(this.product_list[i]);
//            }
        },
    });
});