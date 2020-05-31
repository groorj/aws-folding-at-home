#!/usr/bin/env python

import sys
import yaml
from string import Template


def _get_config_from_file(filename):
    config = {}
    with open(filename, "r") as stream:
        config = yaml.load(stream, Loader=yaml.SafeLoader)
    return config

def _generate_file(template_file, output_file):
    filein = open(template_file)
    src = Template(filein.read())
    file_out = src.substitute(d)
    # print(file_out)
    f = open(output_file, "w")
    f.write(file_out)
    f.close()

# main
if __name__ == "__main__":
    finder_info = []
    default_aws_region = "us-east-1"
    config = _get_config_from_file(sys.argv[1])

    # print("Current configuration:\n", yaml.dump(config, default_flow_style=False))

    aws_profile_name        = config["aws_profile_name"]
    aws_instance_type       = config["aws_instance_type"]
    aws_region              = config["aws_region"]
    aws_availability_zone_1 = config["aws_availability_zone_1"]
    aws_availability_zone_2 = config["aws_availability_zone_2"]
    aws_s3_bucket_name      = config["aws_s3_bucket_name"]
    aws_s3_bucket_region    = config["aws_s3_bucket_region"]
    fah_pass                = config["fah_pass"]
    fah_team_id             = config["fah_team_id"]
    fah_webadmin_port       = config["fah_webadmin_port"]
    fah_user                = config["fah_user"]
    your_ip_address         = config["your_ip_address"]
    aws_tag_fah             = config["aws_tag_fah"]
    aws_ec2_instance_count  = config["aws_ec2_instance_count"]
    enable_stats            = config["enable_stats"]
    
    print("AWS Profile Name: ", aws_instance_type)
    print("AWS Region: ", aws_region)
    print("AWS EC2 Type: ", aws_instance_type)
    print("AWS S3 Bucker Name: ", aws_s3_bucket_name)
    print("Folding@Home User: ", fah_user)
    print("Folding@Home Team Id: ", fah_team_id)
    print("Folding@Home Pass: ", fah_pass)
    print("Whitelist IP Address: ", your_ip_address)
    print("=====")

    d={ 
        'var_fah_user':fah_user, 
        'var_fah_pass':fah_pass,
        'var_fah_team_id':fah_team_id,
        'var_fah_webadmin_port':fah_webadmin_port,
        'var_your_ip_address':your_ip_address,
        'var_aws_region':aws_region,
        'var_aws_availability_zone_1':aws_availability_zone_1,
        'var_aws_availability_zone_2':aws_availability_zone_2,
        'var_aws_profile_name':aws_profile_name,
        'var_aws_instance_type':aws_instance_type,
        'var_aws_s3_bucket_name':aws_s3_bucket_name,
        'var_aws_tag_fah':aws_tag_fah,
        'var_aws_ec2_instance_count':aws_ec2_instance_count,
        'var_aws_s3_bucket_region':aws_s3_bucket_region,
        'var_enable_stats':enable_stats
        } 

    if(enable_stats):
        _generate_file('templates/terraform/iam-ec2.tf.tmpl', 'terraform/iam-ec2.tf')
        var_ec2_instance_profile = "iam_instance_profile        = aws_iam_instance_profile.fah_instance_profile.name"
    else:
        var_ec2_instance_profile = ""
    d['var_ec2_instance_profile'] = var_ec2_instance_profile

    _generate_file('templates/user-data.tmpl', 'bin/user-data.sh')
    _generate_file('templates/terraform/provider.tf.tmpl', 'terraform/provider.tf')
    _generate_file('templates/terraform/network.tf.tmpl', 'terraform/network.tf')
    _generate_file('templates/terraform/compute.tf.tmpl', 'terraform/compute.tf')
    _generate_file('templates/terraform/athena.tf.tmpl', 'terraform/athena.tf')

# End;
