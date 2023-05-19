package org.bigdatainf;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import org.json.JSONObject;


public class TMDB_Mapper extends Mapper<Object, Text, Text, IntWritable> {

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    private String searchTerm = "of"; // Reemplaza "término" con tu término específico

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String jsonString = value.toString();
        JSONObject jsonObject = new JSONObject(jsonString);

        if (jsonObject.has("title") && jsonObject.has("abstract")) {
            String title = jsonObject.getString("title");
            String abstractText = jsonObject.getString("abstract");

            // Busca la aparición del término específico en el abstract
            if (abstractText.toLowerCase().contains(searchTerm.toLowerCase())) {
                word.set(title);
                context.write(word, one);
            }
        }
    }
}