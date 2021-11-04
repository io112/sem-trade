const {createApp, ref, watch} = Vue;

const RVDPicker = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    data() {
        const job_types = [
            {name: 'Гидравлический', value: 'hydro'},
            {name: 'ГУР', value: 'gur'},
            {name: 'Тормозной', value: 'break'},
            {name: 'Кондиционер', value: 'conditioner'},
            {name: 'Сцепление', value: 'gur'},
            {name: 'ГУР', value: 'clutch'},
            {name: 'КПП', value: 'transmission'},
        ];
        const part_types = [
            {name: 'Рукав', value: 'arm'},
            {name: 'Фитинг', value: 'fiting'},
            {name: 'Муфта', value: 'clutch'},
            {name: 'Трубка', value: 'pipe'},
            {name: 'Услуга', value: 'service'},
        ]
        const default_part = {
            type: null,
            id: null,
            parameters: {},
            amount: 0,
            price: 0,
            full_price: 0,
        }

        const default_suggestion = {
            parameters: {},
            parts: [],
        }
        const default_selection = {
            job_type: null,
            items: [],
        }

        const default_selected_part = null

        return {job_types, part_types, default_selection, default_suggestion, default_part, default_selected_part}
    },
    setup() {
        let current_selection = ref({
            job_type: null,
            items: [],
        })
        let subtotal = ref({})
        let suggestion = ref({
            parameters: {},
            parts: [],
        })
        let selected_part = ref(null)
        let part = ref({
            type: null,
            id: null,
            parameters: {},
            amount: 0,
            price: 0,
            full_price: 0,
        })
        let current_part_type = ref()
        let only_present = ref(true)
        let errors = []
        let total_errors = []

        return {
            current_selection,
            current_part_type,
            part,
            selected_part,
            only_present,
            suggestion,
            errors,
            total_errors,
            subtotal,
        };
    },
    mounted() {
        this.resetWatchers();
        this.getSelection();
    },
    components: {
        "p-dropdown": primevue.dropdown,
        "p-inputnumber": primevue.inputnumber,
        "p-inputswitch": primevue.inputswitch,
        "p-inputtext": primevue.inputtext,
    },
    methods: {
        resetWatchers() {
            watch(this.part, (part, prevPart) => {
                this.getItems();
            }, {deep: true});
            watch(this.subtotal, (part, prevPart) => {
                this.updateAmount();
            }, {deep: true});
        },
        async updateRVDType() {
            let resp = await request('/api/make_order/set_job_type', {
                'job_type': this.current_selection.job_type,
            })
            this.updateSelection(resp);
            this.checkErrors();
        },
        setType() {
            this.clearSelection();
            this.getItems();
        }
        ,
        clearSelection() {
            let pt = this.part.type;
            this.suggestion = _.cloneDeep(this.default_suggestion);
            this.selected_part = _.cloneDeep(this.default_selected_part);
            this.part = _.cloneDeep(this.default_part);
            this.part.type = pt;
            this.resetWatchers();
            this.getItems();
        }
        ,
        async getItems() {
            if (this.part.type === 'service') {
                if (!this.selected_part)
                    this.selected_part = {}
                this.part.amount = 1;
                this.selected_part.name = this.part.name;
                this.selected_part.price = this.part.amount;
            } else {
                let resp = await request('/api/make_order/suggest_part', {
                    'only_present': this.only_present,
                    'part_type': this.part.type,
                    'part_params': this.part.parameters,
                });
                this.suggestion.parameters = resp["parameters"];
                this.suggestion.parts = resp["suggestion"];
            }
            if (this.selected_part) {
                this.calcPrice();
                this.checkErrors();
            }
        }
        ,
        checkErrors() {
            this.errors = []
            this.total_errors = []
            if (this.only_present) {
                this.total_errors = this.checkPresence();
            }
            if (this.subtotal.amount <= 0)
                this.total_errors.push("Количество не может быть 0 или меньше")
            if (this.part !== null && this.selected_part !== null) {
                if (this.part.amount > this.selected_part.amount && this.only_present)
                    this.errors.push("Количество не может превышать доступное")
                if (this.part.amount <= 0)
                    this.errors.push("Количество не может быть 0 или меньше")
            }
            if (!this.current_selection.job_type) {
                this.errors.push("Выберите тип рукава");
                this.total_errors.push("Выберите тип рукава");
            }
        }
        ,
        checkPresence() {
            let parts = {};
            let err = [];
            let amount = this.subtotal.amount;
            for (const item of this.current_selection.items) {
                if (!item.item)
                    continue
                if (parts[item.item._id] === undefined) {
                    parts[item.item._id] = item.amount * amount
                } else {
                    parts[item.item._id] += item.amount * amount
                }
            }
            for (const item of this.current_selection.items) {
                if (!item.item)
                    continue
                if (parts[item.item._id] > item.item.amount) {
                    err.push(`На складе не хватает ${item.name}. доступно: ${item.item.amount}, требуется: ${parts[item.item._id]}`)
                }
            }
            return err;
        }
        ,
        async calcPrice() {
            if (this.part.type === 'service') {
                this.part.amount = 1;
                this.part.full_price = this.part.price;
                return
            }
            let resp = await request('/api/make_order/calc_part_price', {
                'part': this.part,
                'type': this.current_selection.job_type,
            })
            this.part.amount = resp['amount'];
            this.part.price = resp['price'];
            this.part.full_price = resp['full_price'];
        }
        ,
        setPart() {
            if (this.selected_part) {
                this.part.parameters = this.selected_part.parameters;
                this.part.type = this.selected_part.type;
                this.part.measure = this.selected_part.measure;
                this.part.id = this.selected_part._id;
            }
        }
        ,
        clearSelectedPart() {
            this.selected_part = null;
            this.part.parameters = {};
            console.log(this.selected_part)
        }
        ,
        clearSelectedParam(paramName) {
            if (this.selected_part)
                alert("Нельзя убрать параметр, когда выбрана деталь")
            else {
                delete (this.part.parameters[paramName])
            }
        }
        ,
        async addItemToSelection() {
            let resp = await request('/api/make_order/add_item_to_selection', {
                'part': this.part,
                'type': this.current_selection.job_type,
            })
            if (resp !== undefined) {
                this.updateSelection(resp);
                this.clearSelection();
            }
        }
        ,
        async getSelection() {
            let resp = await request('/api/make_order/update_selection')
            this.updateSelection(resp);
        }
        ,
        async updateAmount() {
            let resp = await request('/api/make_order/update_amount', {
                'amount': this.subtotal.amount,
            })
            this.updateSelection(resp);
        }
        ,
        async delItem(idx) {
            let resp = await request('/api/make_order/del_selected_part', {
                'item_index': idx
            })
            this.updateSelection(resp);
        }
        ,
        async editItem(idx) {
            let p = this.current_selection.items[idx]
            this.part = p.item
            this.part.measure = p.item.measure
            this.part.parameters = p.item.parameters
            this.part.amount = p.amount
            this.selected_part = p.item
            this.part.id = p.item._id
            this.calcPrice();
            this.resetWatchers();
            let resp = await request('/api/make_order/del_selected_part', {
                'item_index': idx
            })
            this.updateSelection(resp);
        }
        ,
        updateSelection(selection) {
            if (selection !== undefined) {
                this.current_selection.items = selection['items']
                this.current_selection.job_type = selection['subtotal']['job_type']
                this.subtotal = selection['subtotal']
            }
            this.resetWatchers();
            this.checkErrors();
        }
        ,
        async addToCart() {
            let resp = await request('/api/make_order/submit_selection')
            this.clearSelection();
            this.getSelection();
            this.part.type = null;
            this.current_selection.job_type = null;
            $('#addModal').modal('hide');
            update_cart();
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDPicker).use(primevue.config.default).mount('#addModal');
})
