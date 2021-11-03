const {createApp, ref} = Vue;

const RVDPicker = {
    compilerOptions: {
        delimiters: ['[[', ']]'],
        comments: true
    },
    data() {
        const job_types = ref([
            {name: 'Гидравлический', value: 'hydro'},
            {name: 'ГУР', value: 'gur'},
            {name: 'Тормозной', value: 'break'},
            {name: 'Кондиционер', value: 'conditioner'},
            {name: 'Сцепление', value: 'gur'},
            {name: 'ГУР', value: 'clutch'},
            {name: 'КПП', value: 'transmission'},
        ]);
        let part_types = ref([
            {name: 'Рукав', value: 'arm'},
            {name: 'Фитинг', value: 'fiting'},
            {name: 'Муфта', value: 'clutch'},
            {name: 'Услуга', value: 'service'},
        ])
        return {job_types, part_types}
    },
    setup() {
        let current_selection = ref({
            job_type: null,
        })
        let current_part = ref()
        let amount = ref(0)
        let suggestion = ref({
            params: {},
            parts: [],
        })
        let params = ref({})
        let part = ref({
            type: null,
            id: null,
            params: {},
            amount: 0,
            price: 0,
            full_price: 0,
        })
        let current_part_params = ref({})
        let current_part_type = ref()
        let only_preset = ref(true)

        return {current_selection, current_part_type, part, only_preset, current_part_params, suggestion, params};
    },
    mounted() {
    },
    components: {
        "p-dropdown": primevue.dropdown,
        "p-inputnumber": primevue.inputnumber,
    },
    methods: {
        updateSelectionItems() {
            console.log(this.current_selection)
        },
        async getItems() {
            let resp = await request('/api/make_order/suggest_part', {
                'only_present': this.only_present,
                'part_type': this.part.type,
                'part_params': this.part.params,
            });
            this.suggestion.params = resp["parameters"];
            this.suggestion.parts = resp["suggestion"];
            console.log(this.part);

        },
        change() {
        }
    }
}

window.addEventListener("load", () => {
    createApp(RVDPicker).use(primevue.config.default).mount('#rvd-modal-vue-body');
})
