// // document.addEventListener('DOMContentLoaded', function() {
// //     console.log("specification_dynamic_fields.js is loaded and running.");

// //     const updateUnitField = (predefinedNameField, predefinedUnitField) => {
// //         const selectedValue = predefinedNameField.value;
// //         const currentUnitValue = predefinedUnitField.value;

// //         const WEIGHT_UNIT_CHOICES = [
// //             {value: 'kg', text: 'Kilograms'},
// //             {value: 'g', text: 'Grams'},
// //             {value: 'ton', text: 'Tons'},
// //             {value: 'other', text: 'Other'}
// //         ];

// //         const EXPIRY_DATE_UNIT_CHOICES = [
// //             {value: '<2_days', text: 'Less than two days'},
// //             {value: '2-4_days', text: 'Two to four days'},
// //             {value: '>4_days', text: 'More than four days'},
// //             {value: 'other', text: 'Other'}
// //         ];

// //         const resetUnitChoices = (choices, currentValue) => {
// //             predefinedUnitField.innerHTML = '';
// //             let valueFound = false;

// //             choices.forEach(choice => {
// //                 const option = document.createElement('option');
// //                 option.value = choice.value;
// //                 option.text = choice.text;

// //                 if (choice.value === currentValue) {
// //                     option.selected = true;
// //                     valueFound = true;
// //                 }

// //                 predefinedUnitField.appendChild(option);
// //             });

// //             // إذا لم يتم العثور على القيمة الحالية ضمن الخيارات المتاحة
// //             // if (!valueFound && currentValue) {
// //             //     const defaultOption = document.createElement('option');
// //             //     defaultOption.value = currentValue;
// //             //     defaultOption.text = currentValue;
// //             //     defaultOption.selected = true;
// //             //     predefinedUnitField.appendChild(defaultOption);
// //             // }
// //         };

// //         if (selectedValue === 'weight') {
// //             resetUnitChoices(WEIGHT_UNIT_CHOICES, currentUnitValue);
// //         } else if (selectedValue === 'expiry_date') {
// //             resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES, currentUnitValue);
// //         } else {
// //             predefinedUnitField.innerHTML = '<option value="">Select an option</option>';
// //             predefinedUnitField.value = ''; // إعادة تعيين إذا كان الحقل فارغًا
// //         }
// //     };

// //     const initializeFormset = () => {
// //         const formCount = parseInt(document.getElementById('id_specifications-TOTAL_FORMS').value);
// //         for (let i = 0; i < formCount; i++) {
// //             const prefix = `id_specifications-${i}-`;
// //             const predefinedNameField = document.querySelector(`#${prefix}predefined_name`);
// //             const predefinedUnitField = document.querySelector(`#${prefix}predefined_unit`);

// //             if (predefinedNameField && predefinedUnitField) {
// //                 updateUnitField(predefinedNameField, predefinedUnitField);

// //                 predefinedNameField.addEventListener('change', function() {
// //                     updateUnitField(predefinedNameField, predefinedUnitField);
// //                 });
// //             } else {
// //                 console.log(`predefinedName or predefinedUnit field not found for prefix: ${prefix}`);
// //             }
// //         }
// //     };

// //     initializeFormset();

// //     // Listen for new forms added dynamically
// //     document.addEventListener('formset:added', function() {
// //         initializeFormset();
// //     });
// // });





// document.addEventListener('DOMContentLoaded', function() {
//     console.log("specification_dynamic_fields.js is loaded and running.");

//     const updateUnitField = (
//         predefinedNameField, 
//         predefinedUnitField, 
//         predefinedNameField_ar, 
//         predefinedUnitField_ar, 
//         predefinedNameField_en, 
//         predefinedUnitField_en
//     ) => {
//         const selectedValue = predefinedNameField.value || predefinedNameField_ar.value || predefinedNameField_en.value;
//         const currentUnitValue = predefinedUnitField.value || predefinedUnitField_ar.value || predefinedUnitField_en.value;

//         // خيارات الوحدات المترجمة
//         const WEIGHT_UNIT_CHOICES = {
//             en: [
//                 { value: 'kg', text: 'Kilograms' },
//                 { value: 'g', text: 'Grams' },
//                 { value: 'ton', text: 'Tons' },
//                 { value: 'other', text: 'Other' }
//             ],
//             ar: [
//                 { value: 'kg', text: 'كيلوجرامات' },
//                 { value: 'g', text: 'جرامات' },
//                 { value: 'ton', text: 'أطنان' },
//                 { value: 'other', text: 'أخرى' }
//             ]
//         };

//         const EXPIRY_DATE_UNIT_CHOICES = {
//             en: [
//                 { value: '<2_days', text: 'Less than two days' },
//                 { value: '2-4_days', text: 'Two to four days' },
//                 { value: '>4_days', text: 'More than four days' },
//                 { value: 'other', text: 'Other' }
//             ],
//             ar: [
//                 { value: '<2_days', text: 'أقل من يومين' },
//                 { value: '2-4_days', text: 'من يومين إلى أربعة أيام' },
//                 { value: '>4_days', text: 'أكثر من أربعة أيام' },
//                 { value: 'other', text: 'أخرى' }
//             ]
//         };

//         const resetUnitChoices = (choices, currentValue, field) => {
//             field.innerHTML = ''; // مسح الخيارات السابقة
//             choices.forEach(choice => {
//                 const option = document.createElement('option');
//                 option.value = choice.value;
//                 option.text = choice.text;

//                 if (choice.value === currentValue) {
//                     option.selected = true;
//                 }

//                 field.appendChild(option);
//             });
//         };

//         // تحديد الوحدات المعروضة بناءً على القيمة المحددة
//         if (selectedValue === 'weight') {
//             resetUnitChoices(WEIGHT_UNIT_CHOICES.en, currentUnitValue, predefinedUnitField);
//             resetUnitChoices(WEIGHT_UNIT_CHOICES.en, currentUnitValue, predefinedUnitField_en);
//             resetUnitChoices(WEIGHT_UNIT_CHOICES.ar, currentUnitValue, predefinedUnitField_ar);
//         } else if (selectedValue === 'expiry_date') {
//             resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.en, currentUnitValue, predefinedUnitField);
//             resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.en, currentUnitValue, predefinedUnitField_en);
//             resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.ar, currentUnitValue, predefinedUnitField_ar);
//         } else {
//             predefinedUnitField.innerHTML = '<option value="">Select an option</option>';
//             predefinedUnitField_en.innerHTML = '<option value="">Select an option</option>';
//             predefinedUnitField_ar.innerHTML = '<option value="">اختر احد الخيارات</option>';
//             predefinedUnitField.value = '';
//             predefinedUnitField_en.value = '';
//             predefinedUnitField_ar.value = '';
//         }
//     };

//     const synchronizeFields = (field1, field2, field3) => {
//         field2.value = field1.value;
//         field3.value = field1.value;
//     };

//     const initializeFormset = () => {
//         const formCount = parseInt(document.getElementById('id_specifications-TOTAL_FORMS').value);
//         for (let i = 0; i < formCount; i++) {
//             const prefix = `id_specifications-${i}-`;
//             const predefinedNameField = document.querySelector(`#${prefix}predefined_name`);
//             const predefinedUnitField = document.querySelector(`#${prefix}predefined_unit`);
//             const predefinedNameField_ar = document.querySelector(`#${prefix}predefined_name_ar`);
//             const predefinedUnitField_ar = document.querySelector(`#${prefix}predefined_unit_ar`);
//             const predefinedNameField_en = document.querySelector(`#${prefix}predefined_name_en`);
//             const predefinedUnitField_en = document.querySelector(`#${prefix}predefined_unit_en`);

//             if (
//                 predefinedNameField && 
//                 predefinedUnitField && 
//                 predefinedNameField_ar &&
//                 predefinedUnitField_ar &&
//                 predefinedNameField_en &&
//                 predefinedUnitField_en
//             ) {
//                 updateUnitField(
//                     predefinedNameField, 
//                     predefinedUnitField, 
//                     predefinedNameField_ar, 
//                     predefinedUnitField_ar, 
//                     predefinedNameField_en,
//                     predefinedUnitField_en
//                 );

//                 // Synchronize fields when one is changed
//                 predefinedNameField.addEventListener('change', function() {
//                     synchronizeFields(predefinedNameField, predefinedNameField_ar, predefinedNameField_en);
//                     updateUnitField(
//                         predefinedNameField, 
//                         predefinedUnitField, 
//                         predefinedNameField_ar, 
//                         predefinedUnitField_ar, 
//                         predefinedNameField_en,
//                         predefinedUnitField_en
//                     );
//                 });

//                 predefinedNameField_ar.addEventListener('change', function() {
//                     synchronizeFields(predefinedNameField_ar, predefinedNameField, predefinedNameField_en);
//                     updateUnitField(
//                         predefinedNameField, 
//                         predefinedUnitField, 
//                         predefinedNameField_ar, 
//                         predefinedUnitField_ar, 
//                         predefinedNameField_en,
//                         predefinedUnitField_en
//                     );
//                 });

//                 predefinedNameField_en.addEventListener('change', function() {
//                     synchronizeFields(predefinedNameField_en, predefinedNameField, predefinedNameField_ar);
//                     updateUnitField(
//                         predefinedNameField, 
//                         predefinedUnitField, 
//                         predefinedNameField_ar, 
//                         predefinedUnitField_ar, 
//                         predefinedNameField_en,
//                         predefinedUnitField_en
//                     );
//                 });
//             } else {
//                 console.log(`predefinedName or predefinedUnit field not found for prefix: ${prefix}`);
//             }
//         }
//     }
//     initializeFormset();

//     // Listen for new forms added dynamically
//     document.addEventListener('formset:added', function() {
//         initializeFormset();
//     });
// });























document.addEventListener('DOMContentLoaded', function() {
    console.log("specification_dynamic_fields.js is loaded and running.");

    const PREDEFINED_NAME_CHOICES = [
        { value: 'weight', text: 'Weight' },
        { value: 'expiry_date', text: 'Expiry Date' },
        { value: 'fat_content', text: 'Fat Content' },
        { value: 'other', text: 'Other' },
    ];

    const PREDEFINED_NAME_CHOICES_AR = [
        { value: 'weight', text: 'الوزن' },
        { value: 'expiry_date', text: 'تاريخ انتهاء الصلاحية' },
        { value: 'fat_content', text: 'محتوى الدهون' },
        { value: 'other', text: 'أخرى' },
    ];

    const updateUnitField = (
        predefinedNameField, 
        predefinedUnitField, 
        predefinedNameField_ar, 
        predefinedUnitField_ar, 
        predefinedNameField_en, 
        predefinedUnitField_en
    ) => {
        const selectedValue = predefinedNameField.value;
        console.log(`Selected value in updateUnitField: ${selectedValue}`);
    
        const WEIGHT_UNIT_CHOICES = {
            en: [
                { value: 'kg', text: 'Kilograms' },
                { value: 'g', text: 'Grams' },
                { value: 'ton', text: 'Tons' },
                { value: 'other', text: 'Other' }
            ],
            ar: [
                { value: 'kg', text: 'كيلوجرامات' },
                { value: 'g', text: 'جرامات' },
                { value: 'ton', text: 'أطنان' },
                { value: 'other', text: 'أخرى' }
            ]
        };
    
        const EXPIRY_DATE_UNIT_CHOICES = {
            en: [
                { value: '<2_days', text: 'Less than two days' },
                { value: '2-4_days', text: 'Two to four days' },
                { value: '>4_days', text: 'More than four days' },
                { value: 'other', text: 'Other' }
            ],
            ar: [
                { value: '<2_days', text: 'أقل من يومين' },
                { value: '2-4_days', text: 'من يومين إلى أربعة أيام' },
                { value: '>4_days', text: 'أكثر من أربعة أيام' },
                { value: 'other', text: 'أخرى' }
            ]
        };
    
        const resetUnitChoices = (choices, field) => {
            const currentValue = field.value;
            field.innerHTML = ''; // مسح الخيارات السابقة
            choices.forEach(choice => {
                const option = document.createElement('option');
                option.value = choice.value;
                option.text = choice.text;
                if (choice.value === currentValue) {
                    option.selected = true; // تعيين الخيار الحالي كخيار محدد
                }
                field.appendChild(option);
            });
        };
    
        if (selectedValue === 'weight') {
            console.log('Updating weight unit field.');
            resetUnitChoices(WEIGHT_UNIT_CHOICES.en, predefinedUnitField);
            resetUnitChoices(WEIGHT_UNIT_CHOICES.en, predefinedUnitField_en);
            resetUnitChoices(WEIGHT_UNIT_CHOICES.ar, predefinedUnitField_ar);
        } else if (selectedValue === 'expiry_date') {
            console.log('Updating expiry_date unit field.');
            resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.en, predefinedUnitField);
            resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.en, predefinedUnitField_en);
            resetUnitChoices(EXPIRY_DATE_UNIT_CHOICES.ar, predefinedUnitField_ar);
        } else {
            console.log('Clearing unit fields.');
            predefinedUnitField.innerHTML = '<option value="">Select an option</option>';
            predefinedUnitField_en.innerHTML = '<option value="">Select an option</option>';
            predefinedUnitField_ar.innerHTML = '<option value="">اختر احد الخيارات</option>';
        }
    };

       

    const synchronizeFields = (mainField, fieldAr, fieldEn, choicesAr, choicesEn) => {
        const selectedValue = mainField.value;
        console.log(`Synchronizing fields with selected value: ${selectedValue}`);

        const correspondingAr = choicesAr.find(choice => choice.value === selectedValue);
        const correspondingEn = choicesEn.find(choice => choice.value === selectedValue);
        
        console.log('Arabic choice:', correspondingAr);
        console.log('English choice:', correspondingEn);
        
        if (correspondingAr) {
            fieldAr.value = correspondingAr.value;
            fieldAr.innerHTML = `<option value="${correspondingAr.value}">${correspondingAr.text}</option>`;
            console.log(`Assigned Arabic value: ${correspondingAr.text} to ${fieldAr.id}`);
        } else {
            fieldAr.value = '';
            console.log(`No Arabic choice found for value: ${selectedValue}`);
        }

        if (correspondingEn) {
            fieldEn.value = correspondingEn.value;
            fieldEn.innerHTML = `<option value="${correspondingEn.value}">${correspondingEn.text}</option>`;
            console.log(`Assigned English value: ${correspondingEn.text} to ${fieldEn.id}`);
        } else {
            fieldEn.value = '';
            console.log(`No English choice found for value: ${selectedValue}`);
        }
    };

    const initializeFormset = () => {
        const formCount = parseInt(document.getElementById('id_specifications-TOTAL_FORMS').value);
        console.log(`Initializing formset with ${formCount} forms.`);

        for (let i = 0; i < formCount; i++) {
            const prefix = `id_specifications-${i}-`;
            const predefinedNameField = document.querySelector(`#${prefix}predefined_name`);
            const predefinedUnitField = document.querySelector(`#${prefix}predefined_unit`);
            const predefinedNameField_ar = document.querySelector(`#${prefix}predefined_name_ar`);
            const predefinedUnitField_ar = document.querySelector(`#${prefix}predefined_unit_ar`);
            const predefinedNameField_en = document.querySelector(`#${prefix}predefined_name_en`);
            const predefinedUnitField_en = document.querySelector(`#${prefix}predefined_unit_en`);

            console.log(`Processing form with prefix: ${prefix}`);

            if (
                predefinedNameField && 
                predefinedUnitField && 
                predefinedNameField_ar &&
                predefinedUnitField_ar &&
                predefinedNameField_en &&
                predefinedUnitField_en
            ) {
                // تهيئة الحقول المترجمة عند التحميل الأولي
                synchronizeFields(
                    predefinedNameField, 
                    predefinedNameField_ar, 
                    predefinedNameField_en,
                    PREDEFINED_NAME_CHOICES_AR,
                    PREDEFINED_NAME_CHOICES
                );

                updateUnitField(
                    predefinedNameField, 
                    predefinedUnitField, 
                    predefinedNameField_ar, 
                    predefinedUnitField_ar, 
                    predefinedNameField_en,
                    predefinedUnitField_en
                );

                // Synchronize fields when the main field is changed
                predefinedNameField.addEventListener('change', function() {
                    console.log('predefinedNameField changed.');
                    synchronizeFields(
                        predefinedNameField, 
                        predefinedNameField_ar, 
                        predefinedNameField_en,
                        PREDEFINED_NAME_CHOICES_AR,
                        PREDEFINED_NAME_CHOICES
                    );
                    updateUnitField(
                        predefinedNameField, 
                        predefinedUnitField, 
                        predefinedNameField_ar, 
                        predefinedUnitField_ar, 
                        predefinedNameField_en,
                        predefinedUnitField_en
                    );
                });

                predefinedNameField_ar.addEventListener('change', function() {
                    console.log('predefinedNameField_ar changed.');
                    synchronizeFields(
                        predefinedNameField_ar, 
                        predefinedNameField, 
                        predefinedNameField_en,
                        PREDEFINED_NAME_CHOICES_AR,
                        PREDEFINED_NAME_CHOICES
                    );
                    updateUnitField(
                        predefinedNameField, 
                        predefinedUnitField, 
                        predefinedNameField_ar, 
                        predefinedUnitField_ar, 
                        predefinedNameField_en,
                        predefinedUnitField_en
                    );
                });

                predefinedNameField_en.addEventListener('change', function() {
                    console.log('predefinedNameField_en changed.');
                    synchronizeFields(
                        predefinedNameField_en, 
                        predefinedNameField, 
                        predefinedNameField_ar,
                        PREDEFINED_NAME_CHOICES_AR,
                        PREDEFINED_NAME_CHOICES
                    );
                    updateUnitField(
                        predefinedNameField, 
                        predefinedUnitField, 
                        predefinedNameField_ar, 
                        predefinedUnitField_ar, 
                        predefinedNameField_en,
                        predefinedUnitField_en
                    );
                });
            } else {
                console.log(`predefinedName or predefinedUnit field not found for prefix: ${prefix}`);
            }
        }
    };

    initializeFormset();

    // Listen for new forms added dynamically
    document.addEventListener('formset:added', function() {
        console.log('New form added, reinitializing formset.');
        initializeFormset();
    });
});
