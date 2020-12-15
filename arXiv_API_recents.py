import urllib
import feedparser
import codecs

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = 'au:Borodin_A%20OR%20Baik_J%20OR%20Corwin_I%20OR%20Gorin_V%20OR%20Petrov_L%20OR%20Barraquand_G%20OR%20Bufetov_A%20OR%20Kuan_J%20OR%20Rahman_M%20OR%20Shen_H%20OR%20Saenz_A%20OR%20Silva_G%20OR%20Sun_Y%20OR%20Tsai_L%20OR%20Knizel_A%20OR%20Sun_X%20OR%20Dimitrov_E%20OR%20Matetski_K%20OR%20Landon_B%20OR%20Korotkikh_S%20OR%20Peski_R%20OR%20Sitaraman_M%20OR%20Cuenca_C%20OR%20Aggarwal_A%20OR%20Ahn_A%20OR%20Liao_Y%20OR%20Wu_X%20OR%20Ghosal_P%20OR%20Parekh_S%20OR%20Rychnovsky_M%20OR%20Sitaraman_M%20OR%20Liu_Z%20OR%20Matveev_K%20OR%20Moll_A%20OR%20Lin_Y%20OR%20Russkikh_M%20OR%20Prokhorov_A'
start = 0
max_results = 300

query = 'search_query=%s&start=%i&max_results=%i&sortBy=submittedDate&sortOrder=descending' % (search_query,
                                                    start,
                                                    max_results)

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
#  feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
#  feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

# perform a GET request using the base_url and query
response = urllib.request.urlopen(base_url+query).read()

# parse the response using feedparser
feed = feedparser.parse(response)

# print out feed information
print('Feed title: %s' % feed.feed.title)
print('Feed last updated: %s' % feed.feed.updated)

# print opensearch metadata
print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)


# Run through each entry, and print out information
for entry in feed.entries:
    target_file = open (entry.published.split('T')[0] + '-' + entry.id.split('/abs/')[-1].split('v')[0] + '.md', 'w')

    target_file.write('---\n')
    target_file.write('layout: post\n')
    target_file.write('title: ' + entry.id.split('/abs/')[-1].split('v')[0] + ' [' + entry.tags[0]['term'] + ']\n')
    target_file.write('date: ' + entry.published + '\n')
    target_file.write('comments: false\n')
    target_file.write('tags: publication\n')
    target_file.write('published: true\n')
    target_file.write('---\n')
    target_file.write('\n')

    target_file.write('<b>' + '</b>, <b>'.join(author.name for author in entry.authors) + '</b>, "<i>')
    target_file.write(entry.title.replace('\n', '')  + '</i>" ([arXiv](')
    target_file.write(entry.id + '))\n')

    target_file.close()

