const Orders = {
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
        const orders = ref();
        const offset = ref(0);
        const totalRecords = ref(0);
        const rows = ref(15);
        const lazyParams = ref({});
        const sorting = ref('-_number')
        return {dt, orders, loading, totalRecords, lazyParams, rows, offset, sorting}
    },
    mounted() {
        this.loading.value = true;

        this.loadLazyData();
    },
    methods: {
        async loadLazyData() {
            this.loading.value = true;
            let resp = await get(API_ORDERS_GET, {
                limit: this.rows,
                offset: this.offset  * this.rows,
                sorting: this.sorting,
            })
            this.orders = resp.data;
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
        openOrder(order_id) {
            window.location = ORDER_VIEW + order_id
        }
    }
}

window.addEventListener("load", () => {
    createApp(Orders).use(primevue.config.default).mount('#ordersapp');
})