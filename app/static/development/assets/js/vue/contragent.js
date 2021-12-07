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
        emitter.on('newOrder', e => this.getContragent())
    },
    methods: {
        async getContragent() {
            let resp = await get(API_CONTRAGENT_GET)
            if (Object.keys(resp).length !== 0) {
                this.contragent = resp;
                this.query.query = this.contragent['name'] + ' ' + (this.contragent.surname ? this.contragent.surname : '');
                emitter.emit('setContragent', this.contragent)
            } else {
                this.contragent = null
                this.suggestion = []
                this.query.query = ''
                emitter.emit('setContragent', null)
            }
            this.$forceUpdate();
        },
        async setContragent(contragent_id) {
            let resp = await put(API_CONTRAGENT_SET, {
                id: contragent_id,
            })
            this.contragent = resp;
            this.query.query = this.contragent['name'] + ' ' + (this.contragent.surname ? this.contragent.surname : '');
            emitter.emit('setContragent', this.contragent)
            this.$forceUpdate();

        },
        async findContragent() {
            if (this.contragent) {
                return
            }
            let resp = await get(API_CONTRAGENT_FIND, {
                query: this.query.query,
            })
            document.getElementById("client_div").style.display = 'block';
            this.suggestion = resp
        },
        async dropContragent() {
            let resp = await del(API_CONTRAGENT_DEL)
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