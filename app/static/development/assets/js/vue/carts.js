const RVDCarts = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-paginator": primevue.paginator,
        "p-button": primevue.button,
    },
    setup() {
        let data = ref({
            carts: [],
            current_cart_id: "",
            current_cart_idx: 1
        })
        return {data}
    },
    mounted() {
        this.getCarts()
        emitter.on('newOrder', e => this.getCarts())
    },
    methods: {
        async getCarts() {
            let resp = await get(API_CARTS_GET, {'sorting': '+created_at'})
            this.data.carts = resp.data;
            this.data.current_cart_id = Cookies.get('current_order');
            for (let i = 0; i < this.data.carts.length; i++) {
                if (this.data.current_cart_id === this.data.carts[i]._id) {
                    this.data.current_cart_idx = i;
                    break
                }
            }
            this.$forceUpdate();
        },
        async openCart(event) {
            let index = event.page
            Cookies.set('current_order', this.data.carts[index]['_id']);
            emitter.emit('setCart', this.cart)
            setTimeout(() => {
                emitter.emit('newOrder');
                this.getCarts();
                this.$forceUpdate();
            }, 300);
        },
        async createCart() {
            let resp = await get(API_CARTS_CREATE)
            setTimeout(() => {
                emitter.emit('newOrder');
                this.getCarts();
                this.$forceUpdate();
            }, 300);
        },
    }
}

window.addEventListener("load", () => {
    createApp(RVDCarts).use(primevue.config.default).mount('#nav-pager');
})