from django.db import models


class Currency_table(models.Model):
    product = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Product"
    )
    date = models.DateField(
        null=True, blank=True, db_tablespace="Currencies_table", db_column="Date"
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        db_tablespace="Currencies_table",
        db_column="Price",
    )
    day = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Day"
    )
    week = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Week"
    )
    month = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Month"
    )
    quarter = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Quarter"
    )
    year = models.CharField(
        max_length=255, db_tablespace="Currencies_table", db_column="Year"
    )

    class Meta:
        ordering = ("product",)
        db_table = "Currencies_table"
        app_label = "dashboard"

    def __str__(self):
        return self.product


class Currencies(models.Model):
    date = models.DateField(
        null=True, blank=True, db_tablespace="Currencies", db_column="Date"
    )
    product = models.CharField(
        max_length=255, db_tablespace="Currencies", db_column="Material_name"
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        db_tablespace="Currencies",
        db_column="Price",
    )

    class Meta:
        ordering = ("product",)
        db_table = "Currencies"

    def __str__(self):
        return self.product


class Industries(models.Model):
    IndCode = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="IndCode"
    )
    SubInd = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="SubInd"
    )
    SubIndCode = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="SubIndCode"
    )
    Code = models.CharField(
        max_length=255, null=False, db_tablespace="Inds", db_column="Code"
    )
    Name = models.CharField(
        max_length=255, null=False, db_tablespace="Inds", db_column="Name"
    )
    MainIndCode = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="MainIndCode"
    )
    MainIndName = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="MainIndName"
    )
    IndName = models.CharField(
        max_length=255, null=True, db_tablespace="Inds", db_column="IndName"
    )

    class Meta:
        ordering = ("MainIndName",)
        db_table = "Inds"

    def __str__(self):
        return (self.Name,self.SubInd,self.MainIndName)
