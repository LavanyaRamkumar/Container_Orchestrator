var diffHtml = Diff2Html.getPrettyHtml(
    '--- expected \n\
+++ got \n\
@@ -1,4 +1,4 @@\n\
-bacon\n\
+python\n\
eggs\n\
-ham\n\
+hamster\n\
guido\n',
    {inputFormat: 'diff', showFiles: false, matching: 'words', outputFormat: 'side-by-side'}
  );
  document.getElementById("destination-elem-id").innerHTML = diffHtml;