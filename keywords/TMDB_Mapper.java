package org.bigdatainf;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import org.json.JSONObject;


public class TMDB_Mapper extends Mapper<Object, Text, Text, IntWritable> {

    private IntWritable count = new IntWritable(1);
    private Text word = new Text();
    private String[] targetWords = {"paper", "Question", "of"};

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String jsonString = value.toString();
        JSONObject jsonObject = new JSONObject(jsonString);

        if (jsonObject.has("abstract")) {
            String abstractText = jsonObject.getString("abstract").toLowerCase();

            for (String targetWord : targetWords) {
                int frequency = countWordFrequency(abstractText, targetWord);
                count.set(frequency);
                word.set(targetWord);
                context.write(word, count);
            }
        }
    }

    private int countWordFrequency(String text, String targetWord) {
        int count = 0;
        int index = text.indexOf(targetWord);
        while (index != -1) {
            count++;
            index = text.indexOf(targetWord, index + targetWord.length());
        }
        return count;
    }
}