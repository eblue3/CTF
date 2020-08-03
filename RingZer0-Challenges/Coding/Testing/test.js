
        function doRecaptcha() {
            grecaptchaInit('6LfqXXgUAAAAAJ6-DbPq14bFJ9jidApte2w5DU1i', 'hash_crack', $('#Captcha'), $('#btnCrack'));
        }

        grecaptcha.ready(function () {
            doRecaptcha();
        });
        setInterval(function () { doRecaptcha(); }, 1 * 180 * 1000); // just reset every 3 mins

        var totalCracked = 0, totalLeft = 0;

        function tryHash(hash, count) {
            var spanType = $('#type_' + count);
            var spanPass = $('#pass_' + count);
            var spanSalt = $('#salt_' + count);
            var spanMore = $('#more_' + count);
            var captcha = $('#Captcha').val();

            var r = getJSON('/Cracker/API', '{id:"' + hash + '", captcha:"' + captcha + '"}');

            if (r && r.error) {
                notifyMsg('Cracker Error', htmlEncode(r.error), 'danger');
                return false;
            }
            else if (r && r.Cracked == true) {
                var plain = htmlEncode(r.Password).replace(/ /g, '<span class="text-warning">[space]</span>');
                var salt = htmlEncode(r.Salt);

                totalCracked++;
                spanType.html(r.Algorithm);
                spanType.attr('title', 'Hashcat Mode: ' + r.HashcatMode);
                spanPass.html(plain);
                if (r.HashcatMode == 21)
                    spanMore.html('<span class="text-warning">or MD5</span> <span class="text-success">' + salt + plain + '</span>');
                else if (r.HashcatMode == 0 && plain.length > 2 && plain.search(/[0-9a-f]{2}.+/) == 0)
                    spanMore.html('<span class="text-warning">or osCommerce</span> ' + plain.substring(0, 2) + ':<span class="text-success">' + plain.substring(2) + '</span>');
                if (salt.length > 0) spanSalt.html(':' + salt);
            }
            else {
                totalLeft++;
                spanType.html('[No Match]');
                spanType.removeClass('text-warning').addClass('text-danger');
                //pass.html('');
            }

            return true;
        }

        function crackHashes(btn) {
            var txt = $('#txtHashList').val();
            var result = $('#result');

            btn.disabled = true;
            totalCracked = 0;
            totalLeft = 0;

            txt = txt.replace('\r', '');

            var d = txt.split('\n')
            var count = 0;
            var html = '';

            for (var i = 0; i < d.length; i++) {
                for (var j = i + 1; j < d.length; j++) {
                    if (d[j] == d[i]) d[j] = '';
                }
            }

            for (var i = 0; i < d.length; i++)
            {
                if (d[i] == '') continue;
                var h = d[i];
                var p = h.indexOf(':');
                if (p > 0) h = h.substring(0, p);
                if (h.length == 32 || h.length == 40 || h.length == 64 || h.length == 128)
                //if (d[i].length <= 128)
                {
                    html += '<span class="text-info">' + h + '</span>';
                    html += '<span id="salt_' + count + '" class="text-default"></span>';
                    html += ' <span id="type_' + count + '" class="text-warning"><img src="/imgs/working-loader.gif" class="animated-working" /></span>';
                    html += ' <span id="pass_' + count + '" class="text-success"></span> <span id="more_' + count + '"></span><br />';
                    count++;
                }
                else if (d[i].length > 0)
                {
                    html += '<span class="text-danger">' + htmlEncode(d[i]) + ' [Invalid]</span><br />';
                    d[i] = '';
                }
            }

            result.html(html);

            count = 0;
            for (var i = 0; i < d.length; i++) {
                if (d[i].length >= 32) {
                    var ok = tryHash(d[i], count++);
                    if (!ok) break;
                }
            }
            //d.forEach(function (h) {
            //    if (h.length > 0) {
            //        var ok = tryHash(h, count++);
            //        if (!ok) break;
            //    }
            //});

            if (totalCracked == 0)
                notifyMsg('Cracker Result', 'We could not find any matches to your hashes :(', 'danger');
            else {
                var msg = 'We cracked {0} hashes leaving {1} left.';
                msg = msg.replace('{0}', totalCracked);
                msg = msg.replace('{1}', totalLeft);
                notifyMsg('Cracker Result', msg, 'success');
            }

            setTimeout(function () { btn.disabled = false; }, 3000);
        }
