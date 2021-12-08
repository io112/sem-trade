const Carts = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-datatable": primevue.datatable,
        "p-column": primevue.column,
        "p-inputtext": primevue.inputtext
    },
    setup() {
        const dt = ref();
        const loading = ref(false);
        const carts = ref();
        const offset = ref(0);
        const totalRecords = ref(0);
        const rows = ref(15);
        const lazyParams = ref({});
        const sorting = ref('-created_at')
        return {dt, carts, loading, totalRecords, lazyParams, rows, offset, sorting}
    },
    mounted() {
        this.loading.value = true;

        this.loadLazyData();
    },
    methods: {
        async loadLazyData() {
            this.loading.value = true;
            let resp = await get(API_CARTS_GET, {
                limit: this.rows,
                offset: this.offset  * this.rows,
                sorting: this.sorting,
            })
            this.carts = resp.data;
            this.totalRecords = resp.count;
            this.loading.value = false;
        },
        onPage(event) {
            this.offset = event.page
            this.loadLazyData()
        },
        onSort(event) {
            let sortKey = '-'
            if (event.sortOrder === 1) {
                sortKey = '+'
            }
            this.sorting = sortKey + event.sortField
            console.log(this.sorting)
            this.loadLazyData()
        },
        openCart(card_id) {
            Cookies.set('current_order', card_id);
            setTimeout(() => {
                window.location = MAKE_ORDER_URL
            }, 300);
        },
        async deleteCart(cart_id) {
            let resp = await del(API_CARTS_DELETE, {cart_id: cart_id})
            this.loadLazyData();
        }
    }
}

window.addEventListener("load", () => {
    createApp(Carts).use(primevue.config.default).mount('#cartsapp');
})