# Installation et d'exécution de Apache Spark pour l'utilisateur Vagrant

## 🛠️ Installation de Apache Spark

### 1. Télécharger et installer Apache Spark pour Oracle Linux 8

Accédez au répertoire de l'utilisateur `vagrant` :

```bash
cd /home/vagrant
```

Téléchargez directement Apache Spark avec Scala 2.13.X :

```bash
wget https://dlcdn.apache.org/spark/spark-3.5.6/spark-3.5.6-bin-hadoop3.tgz
```

Extraire l'archive :

```bash
tar -xvzf spark-3.5.6-bin-hadoop3.tgz
```

Renommez le dossier extrait :

```bash
mv spark-3.5.6-bin-hadoop3 spark
```

### 2. Lancer Spark Shell

Rajouter les variables d'environnement

```bash
echo 'export SPARK_HOME=/home/vagrant/spark' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Lancer le terminal Spark
```bash
spark-shell
```

# Note: Spark Streaming est une librairie au sein de Spark (Apache Spark)



# 📦 Apache Spark Streaming – Importation dans différents langages de programmation

Apache Spark Streaming est une extension d'Apache Spark permettant le traitement de données en temps réel via des micro-batchs. Il est compatible avec plusieurs langages de programmation, chacun ayant sa propre manière d'importer et d'utiliser cette bibliothèque.

## 🔹 Scala (avec Spark Streaming)

**Explication :**  
Scala est le langage natif de Spark, avec un support complet et natif pour Spark Streaming. On utilise `StreamingContext` pour définir le traitement en continu. Kafka est souvent utilisé comme source de données pour recevoir des flux en temps réel.

**Exemple de code :**
```scala
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._

object SparkStreamingExample {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("SparkStreamingExample")
    val ssc = new StreamingContext(conf, Seconds(10))

    val stream = KafkaUtils.createStream(ssc, "localhost:2181", "spark-streaming-group", Map("topic1" -> 1))

    stream.foreachRDD { rdd =>
      rdd.foreach { record =>
        println(record)
      }
    }

    ssc.start()
    ssc.awaitTermination()
  }
}
```

## 🔹 Java (avec Spark Streaming)

**Explication :**  
Java prend également en charge Spark Streaming via des classes spécifiques comme `JavaStreamingContext`. L'approche est similaire à Scala, avec des classes adaptées à Java.

**Exemple de code :**
```java
import org.apache.spark.SparkConf;
import org.apache.spark.streaming.*;
import org.apache.spark.streaming.kafka.*;

public class SparkStreamingExample {
    public static void main(String[] args) throws Exception {
        SparkConf conf = new SparkConf().setAppName("SparkStreamingExample");
        JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(10));

        JavaInputDStream<ConsumerRecord<String, String>> stream = KafkaUtils.createStream(
            jssc, "localhost:2181", "spark-streaming-group", Map.of("topic1", 1)
        );

        stream.foreachRDD(rdd -> {
            rdd.foreach(record -> {
                System.out.println(record);
            });
        });

        jssc.start();
        jssc.awaitTermination();
    }
}
```

## 🔹 Python (avec PySpark Streaming)

**Explication :**  
PySpark est l'API Python de Spark. Elle permet d'utiliser Spark Streaming avec une syntaxe proche de Scala. Kafka est disponible via des bibliothèques compatibles avec PySpark.

**Exemple de code :**
```python
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def main():
    conf = SparkConf().setAppName("SparkStreamingExample")
    ssc = StreamingContext(conf, 10)

    stream = KafkaUtils.createStream(ssc, "localhost:2181", "spark-streaming-group", {"topic1": 1})
    stream.pprint()

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
```

## 🔹 R (avec Structured Streaming via `sparklyr`)

**Explication :**  
R ne prend pas en charge Spark Streaming traditionnel, mais permet le traitement de flux structurés via le package `sparklyr`. Vous pouvez lire des flux de Kafka et écrire dans des fichiers, mais avec une approche de streaming structuré.

**Exemple de code :**
```r
library(sparklyr)

sc <- spark_connect(master = "local")

streaming_df <- spark_read_stream(sc, name = "streaming_data", 
                                  type = "kafka", 
                                  options = list(topic = "topic1", bootstrap.servers = "localhost:9092"))

streaming_df %>%
  spark_write_stream(path = "output")

streaming_query <- stream_start(streaming_df)

stream_stop(streaming_query)
spark_disconnect(sc)
```

## ✅ Résumé comparatif

| Langage | Support Spark Streaming | Méthode utilisée |
|--------|--------------------------|------------------|
| **Scala**  | ✅ Complet               | `StreamingContext` |
| **Java**   | ✅ Complet               | `JavaStreamingContext` |
| **Python** | ✅ Complet               | `pyspark.streaming` |
| **R**      | ⚠️ Partiel (*Structured Streaming uniquement*) | `sparklyr` |

> 💡 **Schéma général d'utilisation :**  
> Créer un contexte de streaming → définir la source (Kafka, fichiers, sockets…) → appliquer des transformations → lancer avec `start()` → bloquer avec `awaitTermination()`.
---
