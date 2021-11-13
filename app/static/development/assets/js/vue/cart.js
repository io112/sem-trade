const RVDCart = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-datatable": primevue.datatable,
        "p-column": primevue.column,
        "p-button": primevue.button,
    },
    setup() {
        let cart = ref({})
        return {cart}
    },
    mounted() {
        this.getCart()
        emitter.on('updateCart', e => this.updateCart())
    },
    methods: {
        async getCart() {
            let resp = await request('/api/make_order/get_cart', {'sorting': '+last_modified'})
            console.log(resp)
            this.cart = resp;
        },
        async deleteItem(index) {
            let resp = await request('/api/make_order/del_cart_item', {'id': index})
            this.cart = resp;
        },
        async updateCart() {
            this.getCart();
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDCart).use(primevue.config.default).mount('#cart');
})