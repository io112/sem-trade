const RVDCheckout = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {},
    setup() {
        let contragent = null
        let cart = null
        return {contragent, cart}
    },
    mounted() {
        emitter.on('setContragent', contragent => this.setContragent(contragent))
        emitter.on('setCart', e => this.setCart(e))
    },
    methods: {
        async checkout() {
            let resp = get(API_CHECKOUT)
            if (resp) {
                setTimeout(() => {
                    emitter.emit('newOrder');
                }, 300);

            }
        },
        setContragent(contragent) {
            this.contragent = contragent;
            this.$forceUpdate();
        },
        setCart(cart) {
            this.cart = cart;
            this.$forceUpdate();
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDCheckout).use(primevue.config.default).mount('#checkout_list');
})