from django.utils.translation import gettext_lazy as _

PREDEFINED_NAME_CHOICES = [
    ('weight', _('Weight')),
    ('expiry_date', _('Expiry Date')),
    ('fat_content', _('Fat Content')),
    ('other', _('Other')),
]

WEIGHT_UNIT_CHOICES = [
    ('kg', _('Kilograms')),
    ('g', _('Grams')),
    ('ton', _('Tons')),
    ('<2_days', _('Less than two days')),
    ('2-4_days', _('Two to four days')),
    ('>4_days', _('More than four days')),
    ('other', _('Other')),
]

PREDEFINED_NAME_CHOICES_AR = [
    ('weight', 'الوزن'),
    ('expiry_date', 'تاريخ انتهاء الصلاحية'),
    ('fat_content', 'محتوى الدهون'),
    ('other', 'أخرى'),
]

WEIGHT_UNIT_CHOICES_AR = [
    ('kg', 'كيلوجرامات'),
    ('g', 'جرامات'),
    ('ton', 'أطنان'),
    ('<2_days', 'أقل من يومين'),
    ('2-4_days', 'من يومين إلى أربعة أيام'),
    ('>4_days', 'أكثر من أربعة أيام'),
    ('other', 'أخرى'),
]
