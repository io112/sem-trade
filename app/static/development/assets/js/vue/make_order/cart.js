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
        emitter.on('newOrder', e => this.updateCart())
    },
    methods: {
        async getCart() {
            let resp = await get(API_CART_GET, {'sorting': '+last_modified'})
            this.cart = resp;
            emitter.emit('setCart', this.cart)
            this.$forceUpdate();
        },
        async deleteItem(index) {
            let resp = await del(API_CART_DEL, {'id': index})
            this.cart = resp;
            emitter.emit('setCart', this.cart)
            this.$forceUpdate();
        },
        async updateCart() {
            this.getCart();
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDCart).use(primevue.config.default).mount('#cart');
})