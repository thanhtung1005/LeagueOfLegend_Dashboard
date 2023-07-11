class InputDataModal {
    constructor() {
        this.API = null;

        this.$modal = $('#input-modal');
        this.$dialog = this.$modal.find('.modal-dialog')
        this.$title = this.$modal.find('.modal-title');
        this.$body = this.$modal.find('.modal-body');
        this.$form = this.$modal.find('form');
        this.$btnClose = this.$modal.find('.btn-close');
        this.$btnConfirm = this.$modal.find('.btn-confirm');

        this.$inputData = {};
    }

    show() {
        this.$modal.modal('show');
    }

    onChangeInput(disabledCondition) {
        this.$btnConfirm.prop('disabled', disabledCondition);
    }

    clearForm() {
        for (let attr in this.$inputData) {
            this.$inputData[attr].val('');
        };
    }

    getData() {
        let data = {};
        for (let attr in this.$inputData) {
            data[attr] = this.$inputData[attr].val();
        }
        return data;
    }
};


class InputChampionModal extends InputDataModal{
    constructor() {
        super();
        this.$dialog.addClass('modal-xl')
        this.$inputData = {
            'name': this.$form.find('.champion-name'),
            'statHP': this.$form.find('.champion-hp'),
            'statMP': this.$form.find('.champion-mp'),
            'statMoveSpeed': this.$form.find('.champion-move-speed'),
            'statArmor': this.$form.find('.champion-armor'),
            'statAttackRange': this.$form.find('.champion-attack-range'),
            'statAttackDamage': this.$form.find('.champion-attack-damage'),
            'statAttackSpeed': this.$form.find('.champion-attack-speed'),
            'infoAttack': this.$form.find('.champion-info-attack'),
            'infoMagic': this.$form.find('.champion-info-magic'),
            'infoDefense': this.$form.find('.champion-info-defense'),
            'infoDifficulty': this.$form.find('.champion-info-difficulty'),
            'title': this.$form.find('.champion-title'),
            'blurb': this.$form.find('.champion-blurb'),
            // 'classes': this.$form.find('.champion-classes'),
            // 'roles': this.$form.find('.champion-roles'),
        };
    }
}


class InputItemModal extends InputDataModal{
    constructor() {
        super();
        let allTags = [
            '', 'Active', 'Armor', 'ArmorPenetration',
            'AttackSpeed', 'Boots', 'Consumable',
            'CooldownReduction', 'CriticalStrike',
            'Damage', 'GoldPer', 'Health', 'HealthRegen',
            'LifeSteal', 'MagicPenetration', 'Mana', 'ManaRegen',
            'NonbootsMovement', 'OnHit', 'SpellBlock',
            'SpellDamage', 'Trinket', 'Vision',
        ];
        let selectTag = '';
        for (let tag of allTags) {
            selectTag += `<option value="${tag}">${tag}</option>\n`;
        };
        this.$body.append(
            `
            <div class="form-group">
                <label>Name</label>
                <input type="text" class="form-control item-name">
                <label >Buy price</label>
                <input type="number" step="1" min="0" class="form-control item-buy-price">
                <label >Sell price</label>
                <input type="number" step="1" min="0" class="form-control item-sell-price">
                <label >Tag</label>
                <select class="form-control item-tag">
                    ${selectTag}
                </select>
                <label >Explain</label>
                <input type="text" class="form-control item-explain">
            </div>
            `
        )
        this.$inputData = {
            'name': this.$form.find('.item-name'),
            'buyPrice': this.$form.find('.item-buy-price'),
            'sellPrice': this.$form.find('.item-sell-price'),
            'tag': this.$form.find('.item-tag'),
            'explain': this.$form.find('.item-explain'),
        };
    }
}


class InputClassModal extends InputDataModal{
    constructor() {
        super();
        this.$dialog.addClass('modal-sm')
        this.$body.append(
            `
            <div class="form-group">
                <label>Name</label>
                <input type="text" class="form-control class-name">
            </div>
            `
        );
        this.$inputData = {
            'name': this.$form.find('.class-name')
        };
    }
}


class InputRoleModal extends InputDataModal{
    constructor() {
        super();
        this.$dialog.addClass('modal-sm')
        this.$body.append(
            `
            <div class="form-group">
                <label>Name</label>
                <input type="text" class="form-control role-name">
            </div>
            `
        );
        this.$inputData = {
            'name': this.$form.find('.role-name')
        };
    }
}
