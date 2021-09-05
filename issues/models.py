from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.contrib.auth.models import User


class State(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='název')
    mark_issue_as_finished = models.BooleanField(default=False, verbose_name='označit issue jako dokončené')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Stav'
        verbose_name_plural = 'Stavy'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='název')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorie'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def validate_superuser(value):
    user = User.objects.get(id=value)
    if not user.is_superuser:
        raise ValidationError('Pouze superuser může zadávat issue. ')


class Issue(models.Model):
    name = models.CharField(max_length=50, verbose_name='název')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by',
                                verbose_name='zadavatel', validators=[validate_superuser])
    responsible_person = models.ForeignKey(User, on_delete=models.PROTECT, related_name='responsible_person',
                                           verbose_name='řešitel')
    description = models.TextField(verbose_name='popis')
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name='stav')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='kategorie')
    created_at = models.DateTimeField(default=timezone_now(), verbose_name='vytvořeno')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='dokončeno')
    duration = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at', 'name', 'state')
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

    def clean(self):
        # Auto fill the finished_at field for specific State's values
        if self.state.mark_issue_as_finished and (self.finished_at is None):
            self.finished_at = timezone_now()

        # finished_at value can not be earlier than created_at
        if self.finished_at:
            if self.finished_at < self.created_at:
                raise ValidationError('Hodnota <Dokončeno> musí být později než <Vytvořeno>')

        # reset <finished_at> if state is changed to 'unfinished' (self.state.mark_issue_as_finished == False)
        if not self.state.mark_issue_as_finished:
            self.finished_at = None

    def __repr__(self):
        return f'{self.id}-{self.name}'

    def __str__(self):
        return f'{self.created_at.strftime("%Y-%m-%d %H:%M:%S")} - {self.name}'
