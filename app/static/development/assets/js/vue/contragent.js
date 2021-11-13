const RVDContragent = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-inputtext": primevue.inputtext,
        "p-card": primevue.card,
    },
    setup() {
        let contragent = null
        let query = ref({query: ''})
        let suggestion = ref([])
        return {contragent, query, suggestion}
    },
    mounted() {
        watch(this.query, (query, prevQuery) => {
            this.findContragent();
        });
        this.getContragent();
    },
    methods: {
        async getContragent() {
            let resp = await request('/api/make_order/get_contragent')
            if (Object.keys(resp).length !== 0) {
                this.contragent = resp;
                this.query.query = this.contragent['name'] + ' ' + ( this.contragent.surname? this.contragent.surname: '');
                emitter.emit('setContragent', this.contragent)
            }
        },
        async setContragent(contragent_id) {
            let resp = await request('/api/make_order/set_contragent', {
                id: contragent_id,
            })
            this.contragent = resp;
            this.query.query = this.contragent['name'] + ' ' + ( this.contragent.surname? this.contragent.surname: '');
            emitter.emit('setContragent', this.contragent)
            this.$forceUpdate();

        },
        async findContragent() {
            if (this.contragent) {
                return
            }
            let resp = await request('/api/contragent/find_contragents', {
                query: this.query.query,
            })
            document.getElementById("client_div").style.display = 'block';
            this.suggestion = resp
        },
        async dropContragent() {
            let resp = await request('/api/make_order/remove_contragent')
            this.contragent = null
            this.suggestion = []
            this.query.query = ''
            emitter.emit('setContragent', null)
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDContragent).use(primevue.config.default).mount('#contragent');
})