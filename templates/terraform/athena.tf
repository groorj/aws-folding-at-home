resource "aws_glue_catalog_database" "fah_athena_db" {
  name = "fahdb"
}

resource "aws_glue_catalog_table" "fah_athena_db_table" {
  name          = "fah_instances"
  database_name = aws_glue_catalog_database.fah_athena_db.name
  description   = "Table that contains FAH data stored in S3."

  table_type    = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL    = "TRUE"
  }

  storage_descriptor {
    location      = "s3://$var_aws_s3_bucket_name/stats"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "fah-s3-stream"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "instance_id"
      type = "string"
    }
    columns {
      name = "instance_timestamp"
      type = "timestamp"
    }
    columns {
      name = "local_ip"
      type = "string"
    }
    columns { 
      name = "public_ip" 
      type = "string" 
    } 
    columns {
      name = "region"
      type = "string"
    }
    columns {
      name = "az"
      type = "string"
    }
    columns {
      name = "ami_id"
      type = "string"
    }
    columns {
      name = "web_admin_url"
      type = "string"
    }
    columns {
      name = "status"
      type = "string"
    }

  }
}

resource "aws_athena_workgroup" "fah_workgroup" {
  name = "fah-workgroup"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = false

    result_configuration {
      output_location = "s3://$var_aws_s3_bucket_name/stats-athena-output/"
    }
  }
}

resource "aws_athena_named_query" "fah_named_query_select_all" {
  name      = "select_all"
  workgroup = aws_athena_workgroup.fah_workgroup.id
  database  = aws_glue_catalog_database.fah_athena_db.name
  query     = "SELECT * FROM $${aws_glue_catalog_table.fah_athena_db_table.name};"
}
