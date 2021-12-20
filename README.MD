# Preface

Kafkaform is a [Terraform](https://www.terraform.io) like tool for Apache Kafka. It works for Kafka KSQL 5.x only, however the tool was handy in a couple of Kafka related projects and I wanted to share it. The tool allows to: 

- Define the resources which need to be deployed in kafka (connectors, streams, tables, etc) with customizable and reusable templates, by using Jinja2 templating engine.
- Deploy the resources in Kafka. Deployment is idempotent and several precondition checks can be made (eg schema, naming convention, dependencies, etc). This makes straightforward to deploy resources iteratively and migrate pipelines between environments.

Kafka KSQL 6 and above are **NOT** supported. I am not interested in maintaining this tool, if you wanna change it, fork it.

# Installation

- Download this source folder in your system
- Make sure Python 3.8+ is installed
- Install requirements with
  
  ```
  pip3 install -r requirements.txt
  ```

# Usage

1) Define with a configuration file the resources to be deployed. A basic definition file is in ```/test/resources/basic.yml```. In a real world project it is important to make the templates reusable, this achieved with [Jinja2 template engine](https://jinja2docs.readthedocs.io/en/stable). See ```/testit/resources/project``` for a more elaborate project structure. 
2) Use the commands below to manage resources in Kafka.
3) Some commands require certain environment variables set, in case of errors check the error description.

#### Apply

```
./cmd.sh kafka:apply testit/resources/project/raw_de.yml
```

Apply command will update the resources in Kafka to match the resources required by the file. In the current implementation, <b>resources removed from the definition file will not be removed for Kafka</b>. 

This is to allow multiple projects to be deployed in kafka without requiring a central state management system.

#### Plan

```
./cmd.sh kafka:plan testit/resources/project/raw_de.yml
```

Plan shows the actions which would be performed by the apply command, without actually performing any system update.

#### Erase

```
./cmd.sh kafka:erase testit/resources/project/raw_de.yml
```

<b>Warning:</b> Erase removes all listed resources from kafka along with all dependencies.

# Import existing resources

#### Dump

```
./cmd.sh kafka:dump yourfile.yml
```

The dump command imports all the existing Kafka resources in a definition file. The file can be then adapted, saving a lot of time compared to writing all the resources from scratch.

# Debugging

#### Sql

```
./cmd.sh kafka:sql "DESCRIBE EXTENDED KSQL_PROCESSING_LOG;"
```

SQL executes a Kafka KSQL command and shows the result.

#### Debug

```
./cmd.sh config:debug testit/resources/project/raw_de.yml
```

This command will print the resulting resource definition, useful to evaluate the result of macros or debug syntax errors.  