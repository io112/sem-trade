const PartFinder = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    components: {
        "p-dropdown": primevue.dropdown,
        "p-inputtext": primevue.inputtext,
        "p-inputnumber": primevue.inputnumber,
        "p-inputswitch": primevue.inputswitch,
    },
    setup() {
        let form = ref({
            query: '',
            amount: 1,
            only_present: true,
        })
        let selected_service = ref({type: 'service', name: '', amount: 1})
        let items = []
        let selected_part = null
        let price = {}
        let errors = []
        let is_service = ref(false)

        return {
            form,
            items,
            selected_part,
            price,
            errors,
            is_service,
            selected_service
        };
    },
    mounted() {
        watch(this.form, (form, prevForm) => {
            this.searchParts();
            this.countPart();
        });
        watch(this.selected_service, (form, prevForm) => {
            this.processService();
            this.validate();
        });
        this.validate();
    },
    methods: {
        async searchParts() {
            if (this.selected_part)
                return
            let resp = await request('/api/make_order/find_part', {
                'only_present': this.form.only_present,
                'amount': this.form.amount,
                'query': this.form.query,
            });
            this.items = resp['items'];
            this.$forceUpdate();
        },
        async setPart(part) {
            let resp = await request('/api/make_order/calc_item_price', {
                'part': part,
                'amount': this.form.amount,
            });
            if (resp) {
                this.price = resp;
                this.selected_part = part;
                this.validate();
                this.$forceUpdate();
            }
        },
        async countPart() {
            if (this.selected_part) {
                this.setPart(this.selected_part)
            }
        },
        async dropPart() {
            this.selected_part = null;
            this.form.amount = 1;
            this.form.query = '';
            this.price = {};
            this.selected_service.name = '';
            this.selected_service.amount = 1;
            this.is_service = false;
            this.validate();
            this.$forceUpdate();
        },
        async submitPart() {
            this.validate();
            if (this.errors.length !== 0) {
                return
            }
            let resp = ''
            if (!this.is_service)
                resp = await request('/api/make_order/submit_part', {
                    'part': this.selected_part,
                    'amount': this.form.amount,
                });
            else
                resp = await request('/api/make_order/submit_service', {
                    'service': this.selected_service,
                    'amount': this.selected_service['amount'],
                });
            if (resp === "success") {
                $('#addPartModal').modal('hide');
                this.dropPart();
                update_cart();
            }
        },
        validate() {
            this.errors = []
            if (!this.is_service)
                this.validatePart()
            else
                this.validateService();
            this.$forceUpdate();
        },
        validatePart() {
            if (!this.selected_part) {
                this.errors.push('Выберите деталь')
            }
            if (this.form.only_present) {
                if (this.selected_part) {
                    if (this.selected_part.amount < this.form.amount) {
                        this.errors.push("Выбрано больше предметов, чем есть на складе")
                    }
                }
            }
        },
        validateService() {
            if (!this.selected_service.name || this.selected_service.name === '')
                this.errors.push('Укажите название услуги')
        },
        processService() {
            if (this.is_service) {
                this.price.price = this.selected_service.amount
                this.price.full_price = this.selected_service.amount
                this.$forceUpdate();
            }
        }
    }
}

window.addEventListener("load", () => {
    createApp(PartFinder).use(primevue.config.default).mount('#addPartModal');
})